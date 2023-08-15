import inspect
from abc import ABC, ABCMeta, abstractmethod
from functools import wraps
from itertools import zip_longest
from typing import Type, List, TYPE_CHECKING, Dict, Any, Tuple, Callable

from teleapi.core.utils.collectors import CollectorMeta, collect_subclasses
from teleapi.core.utils.syntax import default
from teleapi.types.message import Message
from .exceptions import ParameterParseError
from .params import BaseCommandParameter, CommandParameter
from teleapi.core.utils.collections import clear_none_values

if TYPE_CHECKING:
    from teleapi.core.executors import BaseExecutor


class CommandMeta(CollectorMeta, ABCMeta):
    _collector = {
        'func': collect_subclasses,
        'attributes': {
            BaseCommandParameter: '__dynamic_parameters__'
        }
    }


class BaseCommand(metaclass=CommandMeta):
    # Dynamic generated property, that collects parameters(BaseCommandParameter)
    __dynamic_parameters__: List[Type[BaseCommandParameter]]

    __command_parameters__: List[Type[BaseCommandParameter]] = []

    class Meta:
        pass

    def __init__(self, executor: 'BaseExecutor', name: str = None) -> None:
        self.executor = executor
        self._parameters = [
            parameter_cls(self) for parameter_cls in
            (self.__class__.__dynamic_parameters__ + self.__class__.__command_parameters__)
        ]

        self.name = default(name, getattr(self.__class__.Meta, "name", None))

        if self.name is None:
            raise AttributeError("You must define command name as static property in Meta or in __init__ parameters")

    @classmethod
    def command_parameter(cls, *, name: str, place: int = -1, parser: Callable[[str], Any] = None, **meta_kwargs):
        from teleapi.core.executors.commands import BaseCommand

        def decorator(obj):
            if isinstance(obj, type):
                param_cls_name = f"Parameter__{name}"

                if not issubclass(obj, BaseCommand):
                    raise TypeError(
                        'You can use this decorator only with async functions and subclasses of BaseCommand')
                elif getattr(obj, param_cls_name, None):
                    raise AttributeError(f"Parameter with name '{name}' is already exists")

                async def wrapper(_, value: str) -> Any:
                    return parser(value) if parser else str(value)

                meta = type("Meta", (object,), {'name': name, 'place': place, **meta_kwargs})

                pram_cls = type(param_cls_name, (CommandParameter,), {
                    'parse_value': wrapper,
                    "Meta": meta
                })

                setattr(obj, param_cls_name, pram_cls)
                return obj
            else:
                if not inspect.iscoroutinefunction(obj):
                    raise TypeError('You can use this decorator only with coroutine functions')

                @wraps(obj)
                async def wrapper(param, value) -> Any:
                    return await obj(param.command, value, parameter=param)

                meta = type("Meta", (object,), {'name': name, 'place': place, **meta_kwargs})

                pram_cls = type(obj.__name__, (CommandParameter,), {
                    'parse_value': wrapper,
                    "Meta": meta
                })
                return pram_cls

        return decorator

    async def get_sorted_parameters(self) -> List[BaseCommandParameter]:
        sorted_parameters = []

        for parameter in self._parameters:
            sorted_parameters.insert(parameter.place, parameter)

        return sorted_parameters

    async def parse_parameters(self, args: List[str]) -> Tuple[Dict[str, Any], List[str]]:
        not_parsed = []
        parsed = {}

        parameters = await self.get_sorted_parameters()
        for parameter, argument in zip_longest(parameters, args):
            if argument is None:
                raise ParameterParseError(f"Not enough arguments ({len(parameters)} required, got {len(args)})")
            if parameter is None:
                not_parsed.append(argument)
                continue

            try:
                parsed[parameter.name] = await parameter.parse_value(argument)
            except BaseException as error:
                raise ParameterParseError(f"Failed to parse parameter {parameter}") from error

        return parsed, not_parsed

    async def register_parameter(self, parameter: BaseCommandParameter) -> None:
        if not isinstance(parameter, BaseCommandParameter):
            raise TypeError("parameter must be subclass of BaseCommandParameter")

        self._parameters.append(parameter)

    def unregister_parameter(self, parameter: BaseCommandParameter) -> None:
        self._parameters.remove(parameter)

    @abstractmethod
    async def execute(self, message: Message, **kwargs) -> None:
        ...

    async def ainit(self) -> None:
        ...

    async def before(self, message: Message, **kwargs) -> None:
        ...

    async def after(self, message: Message, **kwargs) -> None:
        ...

    async def process_error(self, error: BaseException, message, **kwargs) -> None:
        raise error

    async def invoke(self, message: Message, **kwargs) -> None:
        await self.before(message, **kwargs)

        try:
            await self.execute(message, **kwargs)
        except BaseException as error:
            await self.process_error(error, message, **kwargs)
        else:
            await self.after(message, **kwargs)


class Command(BaseCommand, ABC):
    pass


def command(*, name: str = None, attr_name: str = None, before=None, after=None, **meta_kwargs):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError('You can use this decorator only with coroutine functions')

        meta = type("Meta", (object,), {'name': default(name, func.__name__), **meta_kwargs})

        command_cls = type(default(attr_name, func.__name__), (Command,), {
            "execute": func,
            "Meta": meta,
            **clear_none_values({
                "before": before,
                "after": after
            })
        })

        return command_cls

    return decorator
