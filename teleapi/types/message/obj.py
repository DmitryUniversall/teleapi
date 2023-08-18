import logging
from datetime import datetime
from typing import TYPE_CHECKING, Union, List

from .model import MessageModel
from teleapi.enums.parse_mode import ParseMode
from ..contact import Contact
from ..poll.sub_object import PollType
from ...core.utils.collections import exclude_from_dict
from ...core.utils.syntax import default

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..reply_keyboard_markup.obj import ReplyKeyboardMarkup
    from ..reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from ...core.ui.inline_view import BaseInlineView
    from ..forece_reply import ForceReply
    from ..message_entity import MessageEntity
    from ..chat.obj import Chat

logger = logging.getLogger(__name__)


class Message(MessageModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Message) and other.id == self.id

    async def reply(self,
                    text: str,
                    message_thread_id: int = None,
                    parse_mode: ParseMode = ParseMode.NONE,
                    disable_web_page_preview: bool = None,
                    disable_notification: bool = None,
                    protect_content: bool = None,
                    allow_sending_without_reply: bool = None,
                    ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        return await self.chat.send_message(**payload)

    async def reply_photo(self,
                          photo: Union[bytes, str],
                          message_thread_id: int = None,
                          caption: str = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          has_spoiler: bool = None,
                          disable_notification: bool = None,
                          protect_content: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        return await self.chat.send_photo(**payload)

    async def reply_audio(self,
                          audio: Union[bytes, str],
                          message_thread_id: int = None,
                          caption: str = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          duration: int = None,
                          performer: str = None,
                          title: str = None,
                          thumbnail: Union[bytes, str] = None,
                          disable_notification: bool = None,
                          protect_content: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_audio(**payload)

    async def reply_document(self,
                             document: Union[bytes, str],
                             message_thread_id: int = None,
                             caption: str = None,
                             parse_mode: ParseMode = ParseMode.NONE,
                             caption_entities: List['MessageEntity'] = None,
                             disable_content_type_detection: bool = None,
                             thumbnail: Union[bytes, str] = None,
                             disable_notification: bool = None,
                             protect_content: bool = None,
                             allow_sending_without_reply: bool = None,
                             view: 'BaseInlineView' = None,
                             filename: str = None,
                             reply_markup: Union[
                                 'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                             ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_document(**payload)

    async def reply_video(self,
                          video: Union[bytes, str],
                          thumbnail: Union[bytes, str] = None,
                          message_thread_id: int = None,
                          caption: str = None,
                          duration: int = None,
                          height: int = None,
                          width: int = None,
                          has_spoiler: bool = None,
                          supports_streaming: bool = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          disable_notification: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_video(**payload)

    async def reply_video_note(self,
                               video_note: Union[bytes, str],
                               message_thread_id: int = None,
                               duration: int = None,
                               length: int = None,
                               protect_content: bool = None,
                               disable_notification: bool = None,
                               allow_sending_without_reply: bool = None,
                               reply_markup: Union[
                                   'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                               view: 'BaseInlineView' = None
                               ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_video_note(**payload)

    async def reply_poll(self,
                         question: str,
                         options: List[str] = None,
                         is_anonymous: bool = None,
                         type_: PollType = None,
                         allows_multiple_answers: bool = None,
                         correct_option_id: int = None,
                         explanation: str = None,
                         explanation_parse_mode: ParseMode = ParseMode.NONE,
                         explanation_entities: List['MessageEntity'] = None,
                         open_period: int = None,
                         close_date: datetime = None,
                         is_closed: bool = None,
                         disable_notification: bool = None,
                         protect_content: bool = None,
                         allow_sending_without_reply: bool = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         view: 'BaseInlineView' = None
                         ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_poll(**payload)

    async def reply_contact(self,
                            contact: 'Contact',
                            disable_notification: bool = None,
                            protect_content: bool = None,
                            allow_sending_without_reply: bool = None,
                            reply_markup: Union[
                                'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                            view: 'BaseInlineView' = None
                            ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_contact(**payload)

    async def reply_dice(self,
                         emoji: 'str' = None,
                         disable_notification: bool = None,
                         protect_content: bool = None,
                         allow_sending_without_reply: bool = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         view: 'BaseInlineView' = None
                         ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self

        return await self.chat.send_dice(**payload)

    async def forward(self,
                      to_chat: Union['Chat', int, str],
                      message_thread_id: int = None,
                      disable_notification: bool = None,
                      protect_content: bool = None
                      ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self

        return await self.chat.forward_message(**payload)

    async def edit_text(self,
                        text: str,
                        inline_message_id: int = None,
                        parse_mode: ParseMode = ParseMode.NONE,
                        disable_web_page_preview: bool = None,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None,
                        keep_reply_markup: bool = False,
                        entities: List['MessageEntity'] = None
                        ) -> Union['Message', bool]:
        if keep_reply_markup:
            if not self.reply_markup:
                logger.warning(
                    f"reply_markup argument is specified in Message.edit_text call, but message ({self.id}) object didnt have 'reply_markup' attribute defined before")
            else:
                reply_markup = self.reply_markup

        payload = exclude_from_dict(locals(), 'self', 'keep_reply_markup')
        payload['message'] = self

        return await self.chat.edit_message_text(**payload)

    async def copy(self,
                   to_chat: Union['Chat', int, str],
                   disable_notification: bool = None,
                   protect_content: bool = None,
                   reply_to_message: Union[int, 'Message'] = None,
                   caption: str = None,
                   caption_entities: List['MessageEntity'] = None,
                   parse_mode: ParseMode = ParseMode.NONE,
                   allow_sending_without_reply: bool = None,
                   reply_markup: Union[
                       'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                   ) -> int:
        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self
        payload['reply_to_message'] = reply_to_message if isinstance(reply_to_message,
                                                                     int) or reply_to_message is None else reply_to_message.id
        payload['caption'] = default(caption, self.caption)
        payload['caption_entities'] = default(caption_entities, self.caption_entities)
        payload['reply_markup'] = default(reply_markup, self.reply_markup)

        return await self.chat.copy_message(**payload)
