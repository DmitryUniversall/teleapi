from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING
from teleapi.core.utils.syntax import default

if TYPE_CHECKING:
    from teleapi.core.executors.commands import BaseCommand


class BaseCommandParameter(ABC):
    class Meta:
        pass

    def __init__(self, command: 'BaseCommand', name: str = None, place: int = None) -> None:
        self.command = command
        self.name = default(name, getattr(self.__class__.Meta, "name", None))
        self.place = default(place, getattr(self.__class__.Meta, "place", -1))

        if self.name is None:
            raise AttributeError("You must define parameter name as static property in Meta or in __init__ parameters")

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{self.name} at {self.place}]>"

    @abstractmethod
    async def parse_value(self, value: str) -> Any:
        ...


class CommandParameter(BaseCommandParameter, ABC):
    async def parse_value(self, value: str) -> Any:
        return value
