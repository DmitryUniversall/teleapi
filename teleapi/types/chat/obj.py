from datetime import datetime
from typing import TYPE_CHECKING, Union, List

from teleapi.core.http.request import method_request
from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.utils.collections import exclude_from_dict
from teleapi.enums.chat_action import ChatAction
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.user import User
from .model import ChatModel
from ..chat_member.sub_objects.administrator import ChatAdministrator, ChatAdministratorSerializer
from ..message_entity import MessageEntity
from ..poll.sub_object import PollType
from ...generics.http.methods.messages import send_message, edit_message_text, send_photo, copy_message, \
    forward_message, send_audio, send_document, send_video, send_video_note, send_poll
from ..chat_member import ChatMember, ChatMemberObjectSerializer
from .exceptions import BadChatType

if TYPE_CHECKING:
    from teleapi.types.message.obj import Message
    from ...core.ui.inline_view.view import BaseInlineView
    from ..forece_reply import ForceReply
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..reply_keyboard_markup import ReplyKeyboardMarkup
    from ..reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove


class Chat(ChatModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Chat) and other.id == self.id

    @classmethod
    async def get_chat(cls, chat_id: Union[int, str]) -> 'Chat':
        """
        Gets information about a chat.

        :param chat_id: Union[int, str]
            The unique identifier of the chat. This can be either an integer chat ID or a string representing a chat username.

        :return: 'Chat'
            An instance of the 'Chat' class.

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        from teleapi.types.chat.serializer import ChatSerializer

        response, data = await method_request("GET", APIMethod.GET_CHAT, data={'chat_id': chat_id})
        return ChatSerializer().serialize(data=data['result'])

    async def get_member(self, user: Union[int, User]) -> 'ChatMember':
        """
        Gets information about a chat member.

        :param user: `Union[int, User]`
            User to be banned from the chat. Can be provided as User instance or id

        :return: 'ChatMember'
            An instance of the 'ChatMember' class, or any of its subclasses (sub_objects).

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        response, data = await method_request("GET", APIMethod.GET_CHAT_MEMBER, data={
            'chat_id': self.id,
            'user_id': user if isinstance(user, int) else user.id
        })
        return ChatMemberObjectSerializer().serialize(data=data['result'])

    async def get_administrators(self) -> List['ChatAdministrator']:
        """
        Use this method to get a list of administrators in a chat, which aren't bots.

        :return: `List[ChatMember]`
             Array of ChatAdministrator objects

        Notes:
         - If your bot is administrator - it will also be returned

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """
        if self.type_ == 'private':  # TODO: Chat type enum
            raise BadChatType("There are no administrators in the private chat")

        response, data = await method_request("GET", APIMethod.GET_CHAT_ADMINISTRATORS, data={'chat_id': self.id})
        return ChatAdministratorSerializer().serialize(data=data['result'], many=True)

    async def get_member_count(self) -> int:
        """
        Gets the count of members in the chat.

        :return: 'int'
            The count of members in the chat.

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        if self.type_ == 'private':
            return 2

        response, data = await method_request("GET", APIMethod.GET_CHAT_MEMBERS_COUNT, data={'chat_id': self.id})
        return int(data['result'])

    async def leave(self) -> bool:
        """
        Use this method for your bot to leave a group, supergroup or channel. Returns True on success.

        :return: 'bool'
            Returns True on success.

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        response, data = await method_request("GET", APIMethod.LEAVE_CHAT, data={'chat_id': self.id})

        return bool(data['result'])

    async def send_action(self, action: ChatAction, message_thread_id: int = None) -> bool:
        """
        Sends a chat action to indicate the current status of the bot in the chat.

        :param action: `ChatAction`
            The type of chat action to send, indicating the current status or action.
        :param message_thread_id: `int`
            (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

        :return: `bool`
            Returns True if the action was successfully sent

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        payload = exclude_from_dict(locals(), 'self')
        payload['chat_id'] = self.id
        payload['action'] = action.value

        response, data = await method_request("POST", APIMethod.SEND_CHAT_ACTION, data=payload)
        return bool(data)

    async def ban_member(self, user: Union[int, User], until_date: datetime = None,
                         revoke_messages: bool = None) -> bool:
        """
        Bans a member

        :param user: `Union[int, User]`
            User to be banned from the chat. Can be provided as User instance or id
        :param until_date: `datetime`
            (Optional) The date and time until which the ban will be active. If not provided, the ban will be permanent.
        :param revoke_messages: `bool`
            (Optional) Pass True to delete all messages from the chat for the user that is being removed

        :return: `bool`
            Returns True if the user was successfully banned

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        payload = exclude_from_dict(locals(), 'self')
        payload['until_date'] = until_date.timestamp()
        payload['chat_id'] = self.id
        payload['user_id'] = user if isinstance(user, int) else user.id

        response, data = await method_request("POST", APIMethod.BAN_CHAT_MEMBER, data=payload)
        return bool(data)

    async def unban_member(self, user: Union[int, User], only_if_banned: bool = None) -> bool:
        """
        Unbans a member

        :param user: `Union[int, User]`
            User to be banned from the chat. Can be provided as User instance or id
        :param only_if_banned: `bool`
            (Optional) Do nothing if the user is not banned

        :return: `bool`
            Returns True if the user was successfully unbanned

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        payload = exclude_from_dict(locals(), 'self')
        payload['chat_id'] = self.id
        payload['user_id'] = user if isinstance(user, int) else user.id

        response, data = await method_request("GET", APIMethod.UNBAN_CHAT_MEMBER, data=payload)
        return bool(data)

    async def send_message(self,
                           text: str,
                           reply_to_message: Union[int, 'Message'] = None,
                           message_thread_id: int = None,
                           parse_mode: ParseMode = ParseMode.NONE,
                           disable_web_page_preview: bool = None,
                           disable_notification: bool = None,
                           protect_content: bool = None,
                           allow_sending_without_reply: bool = None,
                           reply_markup: Union[
                               'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                           entities: List[MessageEntity] = None,
                           view: 'BaseInlineView' = None
                           ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_message
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_message(**payload)

    async def send_photo(self,
                         photo: Union[bytes, str],
                         message_thread_id: int = None,
                         caption: str = None,
                         parse_mode: ParseMode = ParseMode.NONE,
                         caption_entities: List[MessageEntity] = None,
                         has_spoiler: bool = None,
                         disable_notification: bool = None,
                         protect_content: bool = None,
                         reply_to_message: Union[int, 'Message'] = None,
                         allow_sending_without_reply: bool = None,
                         view: 'BaseInlineView' = None,
                         filename: str = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                         ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_photo
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_photo(**payload)

    async def send_audio(self,
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
                         reply_to_message: Union[int, 'Message'] = None,
                         allow_sending_without_reply: bool = None,
                         view: 'BaseInlineView' = None,
                         filename: str = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                         ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_audio
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_audio(**payload)

    async def send_document(self,
                            document: Union[bytes, str],
                            message_thread_id: int = None,
                            caption: str = None,
                            parse_mode: ParseMode = ParseMode.NONE,
                            caption_entities: List['MessageEntity'] = None,
                            disable_content_type_detection: bool = None,
                            thumbnail: Union[bytes, str] = None,
                            disable_notification: bool = None,
                            protect_content: bool = None,
                            reply_to_message: Union[int, 'Message'] = None,
                            allow_sending_without_reply: bool = None,
                            view: 'BaseInlineView' = None,
                            filename: str = None,
                            reply_markup: Union[
                                'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                            ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_document
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_document(**payload)

    async def send_video(self,
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
                         reply_to_message: Union[int, 'Message'] = None,
                         allow_sending_without_reply: bool = None,
                         view: 'BaseInlineView' = None,
                         filename: str = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                         ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_video
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_video(**payload)

    async def send_video_note(self,
                              video_note: Union[bytes, str],
                              message_thread_id: int = None,
                              duration: int = None,
                              length: int = None,
                              protect_content: bool = None,
                              disable_notification: bool = None,
                              reply_to_message: Union[int, 'Message'] = None,
                              allow_sending_without_reply: bool = None,
                              reply_markup: Union[
                                  'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                              view: 'BaseInlineView' = None
                              ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_video_note
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_video_note(**payload)

    async def send_poll(self,
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
                        reply_to_message: Union[int, 'Message'] = None,
                        allow_sending_without_reply: bool = None,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None
                        ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.send.send_poll
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_poll(**payload)

    async def edit_message_text(self,
                                text: str,
                                message: Union[int, 'Message'],
                                inline_message_id: int = None,
                                parse_mode: ParseMode = ParseMode.NONE,
                                disable_web_page_preview: bool = None,
                                reply_markup: Union[
                                    'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                entities: List[MessageEntity] = None,
                                view: 'BaseInlineView' = None
                                ) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.edit.edit_message_text
        """

        payload = exclude_from_dict(locals(), 'self', 'message')
        payload['chat_id'] = self.id
        payload['message_id'] = message if isinstance(message, int) or message is None else message.id

        return await edit_message_text(**payload)

    async def copy_message(self,
                           to_chat: Union['Chat', int, str],
                           message: Union['Message', int],
                           disable_notification: bool = None,
                           protect_content: bool = None,
                           reply_to_message: Union[int, 'Message'] = None,
                           caption: str = None,
                           caption_entities: List[MessageEntity] = None,
                           parse_mode: ParseMode = ParseMode.NONE,
                           allow_sending_without_reply: bool = None,
                           reply_markup: Union[
                               'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                           ) -> int:
        """
        Abbreviation for the teleapi.generics.http.methods.messages.forward.copy_message
        """

        payload = exclude_from_dict(locals(), 'self', 'to_chat', 'message', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['to_chat_id'] = to_chat.id if isinstance(to_chat, Chat) else to_chat
        payload['message_id'] = message if isinstance(message, int) else message.id
        payload['chat_id'] = self.id
        return await copy_message(**payload)

    async def forward_message(self,
                              message: Union['Message', int],
                              to_chat: Union['Chat', int, str],
                              message_thread_id: int = None,
                              disable_notification: bool = None,
                              protect_content: bool = None) -> 'Message':
        """
        Abbreviation for the teleapi.generics.http.methods.messages.forward.forward_message
        """

        payload = exclude_from_dict(locals(), 'self', 'to_chat', 'message', 'reply_to_message')
        payload['to_chat_id'] = to_chat.id if isinstance(to_chat, Chat) else to_chat
        payload['message_id'] = message if isinstance(message, int) else message.id
        payload['chat_id'] = self.id
        return await forward_message(**payload)
