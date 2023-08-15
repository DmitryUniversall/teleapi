from abc import ABC, abstractmethod
from teleapi.types.update.obj import Update
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from teleapi.core.bots.bot import BaseBot


class BaseMiddleware(ABC):
    def __init__(self, bot: 'BaseBot') -> None:
        self.bot = bot

    async def ainit(self) -> None:
        ...

    @abstractmethod
    async def pre_process(self, update: Update) -> Update:
        ...

    @abstractmethod
    async def post_process(self, update: Update) -> None:
        ...
