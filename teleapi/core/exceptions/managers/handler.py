import inspect
from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING
from teleapi.types.update import Update
from functools import wraps

if TYPE_CHECKING:
    from .manager import BaseErrorManager


class BaseErrorHandler(ABC):
    def __init__(self, manager: 'BaseErrorManager') -> None:
        self.manager = manager

    @property
    @abstractmethod
    def exception_cls(self) -> Type[BaseException]:
        ...

    @abstractmethod
    async def handle(self, error: BaseException, update: Update) -> bool:
        ...


class ErrorHandler(BaseErrorHandler, ABC):
    pass


def handler(*, exception_cls: Type[BaseException]):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("You can use this decorator only with coroutine functions")

        @wraps(func)
        async def wrapper(h, *args, **kwargs):
            return await func(h.manager, *args, **kwargs, handler=h)

        handler_cls = type(func.__name__, (ErrorHandler,), {"handle": wrapper, "exception_cls": exception_cls})
        return handler_cls

    return decorator
