from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from teleapi.core.http.updaters.events import AllowedUpdates, AllowedUpdates_default
from teleapi.core.utils.syntax import default

if TYPE_CHECKING:
    from teleapi.core.bots.bot import BaseBot
    from teleapi.types.update.obj import Update


class BaseUpdater(ABC):
    def __init__(self, *, bot: 'BaseBot', allowed_updates: List[AllowedUpdates] = None) -> None:
        self.bot = bot
        self.allowed_updates = default(allowed_updates, AllowedUpdates_default)

    async def ainit(self) -> None:
        ...

    @abstractmethod
    async def get_updates(self) -> List['Update']:
        ...


class Updater(BaseUpdater, ABC):
    pass
