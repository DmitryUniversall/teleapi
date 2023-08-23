import asyncio
from teleapi.core.http.updaters.updater import BaseUpdater
from teleapi.core.http.updaters.events import UpdateEvent, AllowedUpdates
from typing import Type, List, Dict
from teleapi.core.bots.middlewares import BaseMiddleware
from teleapi.core.utils.syntax import default
from teleapi.generics.http.methods.bot import get_me
from teleapi.types.chat.chat_type import ChatType
from teleapi.types.update.obj import Update
from abc import ABC, abstractmethod
from teleapi.core.executors.executor import BaseExecutor
from teleapi.core.state.settings import project_settings
import re
from teleapi.core.exceptions.managers import BaseErrorManager, ErrorManager
import logging

logger = logging.getLogger(__name__)


class BaseBot(ABC):
    __bot_middlewares__: List[Type[BaseMiddleware]] = []
    __bot_executors__: List[Type[BaseExecutor]] = []

    def __init__(self, updater_cls: Type[BaseUpdater], error_manager: BaseErrorManager = None, allowed_updates: List[AllowedUpdates] = None) -> None:
        self._is_initialized = False
        self.me = None
        self.error_manager = default(error_manager, ErrorManager())
        self.updater = updater_cls(bot=self, allowed_updates=allowed_updates)

        self.__middlewares: List[BaseMiddleware] = [
            middleware_cls(self) for middleware_cls in (project_settings.get('MIDDLEWARES', []) + self.__class__.__bot_middlewares__)
        ]
        self._executors: List[BaseExecutor] = [
            executor_cls(self) for executor_cls in (project_settings.get('EXECUTORS', []) + self.__class__.__bot_executors__)
        ]

        project_settings.BOT = self

    @abstractmethod
    async def dispatch(self, update: Update) -> None:
        ...

    def get_regex_command_prefix(self) -> Dict[str, str]:
        return {
            'group': f"^/(\w+)@{self.me.username}",
            'private': f'^/(\w+)'
        }

    async def ainit(self) -> None:
        if self._is_initialized:
            raise RuntimeError('Bot is already initialized')

        await self.updater.ainit()

        self.me = await get_me()

        for middleware in self.__middlewares:
            await middleware.ainit()

        for executor in self._executors:
            asyncio.create_task(executor.ainit())

        logger.info(f"Bot was successfully initialized")
        self._is_initialized = True

    async def register_executor(self, executor: BaseExecutor) -> None:
        if not isinstance(executor, BaseExecutor):
            raise TypeError("executor must be instance of BaseExecutor")

        await executor.ainit()
        self._executors.append(executor)

        logger.debug(f"Registered executor {executor} ({type(executor)})")

    def unregister_executor(self, executor: BaseExecutor) -> None:
        self._executors.remove(executor)

        logger.debug(f"Unregistered executor {executor}")

    async def register_middleware(self, middleware: BaseMiddleware) -> None:
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError("middleware must be instance of BaseMiddleware")

        await middleware.ainit()
        self.__middlewares.append(middleware)

        logger.debug(f"Registered middleware {middleware} ({type(middleware)})")

    def unregister_middleware(self, middleware: BaseMiddleware) -> None:
        self.__middlewares.remove(middleware)

        logger.debug(f"Unregistered middleware {middleware}")

    async def call_event(self, update: Update, event_type: UpdateEvent, **kwargs) -> None:
        logger.debug(f"Calling event {event_type} on update {update.id}")

        tasks = [executor.call_event(update, event_type, **kwargs) for executor in self._executors]

        for task in asyncio.as_completed(tasks):
            try:
                await task
            except BaseException as error:
                asyncio.create_task(self.error_manager.process_error(error, update))

    async def process_update(self, update: Update) -> None:
        logger.info(f"Processing update {update.id}")

        for middleware in self.__middlewares:
            update = await middleware.pre_process(update)

        await self.dispatch(update)

        for middleware in self.__middlewares:
            await middleware.post_process(update)

    async def _invoke_update(self, update: Update) -> None:
        if not self._is_initialized:
            raise RuntimeError("Bot is not initialized yet. Call 'ainit' method before use this")

        try:
            await self.process_update(update)
        except BaseException as error:
            await self.error_manager.process_error(error, update)

    async def run(self):
        logger.info(f"Starting bot with debug: {project_settings.DEBUG}")

        if not self._is_initialized:
            await self.ainit()

        while True:
            updates = await self.updater.get_updates()

            if updates:
                for update in updates:
                    asyncio.create_task(self._invoke_update(update))


class Bot(BaseBot):
    async def dispatch(self, update: Update) -> None:
        if update.message:
            if update.message.text and update.message.entities and update.message.entities[0].type_ == 'bot_command' and update.message.entities[0].offset == 0:
                if update.message.chat.type_ == ChatType.PRIVATE:
                    if match := re.match(self.get_regex_command_prefix()['private'], update.message.text):
                        asyncio.create_task(
                            self.call_event(update, UpdateEvent.ON_COMMAND, message=update.message, command_name=match.group(1))
                        )
                else:
                    if match := re.match(self.get_regex_command_prefix()['group'], update.message.text):
                        asyncio.create_task(
                            self.call_event(update, UpdateEvent.ON_COMMAND, message=update.message, command_name=match.group(1))
                        )

            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_MESSAGE, message=update.message)
            )
        if update.channel_post:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHANNEL_POST, post=update.channel_post)
            )
        if update.callback_query:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CALLBACK_QUERY, callback_query=update.callback_query)
            )
        if update.chat_member:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHAT_MEMBER_UPDATED, member_update=update.chat_member)
            )
        if update.bot_chat_member:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_BOT_CHAT_MEMBER_UPDATED, bot_member_update=update.bot_chat_member)
            )
        if update.poll:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_POLL_STATUS_UPDATED, poll=update.poll)
            )
        if update.poll_answer:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_POLL_ANSWER, answer=update.poll_answer)
            )
        if update.chat_join_request:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHAT_JOIN_REQUEST, answer=update.chat_join_request)
            )
