from datetime import datetime
from typing import TYPE_CHECKING, Union, List

from teleapi.core.http.request import method_request
from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.utils.collections import exclude_from_dict
from teleapi.enums.chat_action import ChatAction
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.user import User
from .exceptions import BadChatType
from .model import ChatModel
from ..chat_member import ChatMember, ChatMemberObjectSerializer
from ..chat_member.sub_objects.administrator import ChatAdministrator, ChatAdministratorSerializer
from ..chat_permissions import ChatPermissions, ChatPermissionsSerializer
from ..contact import Contact
from ..input_media.sub_objects.audio import InputMediaAudio
from ..input_media.sub_objects.document import InputMediaDocument
from ..input_media.sub_objects.photo import InputMediaPhoto
from ..input_media.sub_objects.video import InputMediaVideo
from ..message_entity import MessageEntity
from ..poll.sub_object import PollType
from ...generics.http.methods.messages import *
from teleapi.types.chat_invite_link import ChatInviteLink, ChatInviteLinkSerializer

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

    async def restrict_member(self,
                              user: Union[int, User],
                              permissions: ChatPermissions,
                              use_independent_chat_permissions: bool = None,
                              until_date: datetime = None
                              ) -> bool:
        """
        Description

        :param user: `Union[int, User]`
            User to be restricted

        :param permissions: `ChatPermissions`
            New user permissions

        :param use_independent_chat_permissions: `bool`
            Pass True if chat permissions are set independently.
            Otherwise, the can_send_other_messages and can_add_web_page_previews permissions
            will imply the can_send_messages, can_send_audios, can_send_documents,
            can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions;
            the can_send_polls permission will imply the can_send_messages permission.

        :param until_date: `datetime`
            Date when restrictions will be lifted for the user, unix time.
            If user is restricted for more than 366 days or less than 30 seconds from the current time,
            they are considered to be restricted forever

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.RESTRICT_CHAT_MEMBER, data={
            'chat_id': self.id,
            'user_id': user if isinstance(user, int) else user.id,
            'permissions': ChatPermissionsSerializer().serialize(obj=permissions),
            'use_independent_chat_permissions': use_independent_chat_permissions,
            'until_date': until_date.timestamp()
        })

        return bool(data['result'])

    async def promote_member(self,
                             user: Union[int, User],
                             is_anonymous: bool = None,
                             can_manage_chat: bool = None,
                             can_post_messages: bool = None,
                             can_edit_messages: bool = None,
                             can_delete_messages: bool = None,
                             can_manage_video_chats: bool = None,
                             can_restrict_members: bool = None,
                             can_promote_members: bool = None,
                             can_change_info: bool = None,
                             can_invite_users: bool = None,
                             can_pin_messages: bool = None,
                             can_manage_topics: bool = None,
                             ) -> bool:
        """
        Promote a member to an administrator in the chat with specified privileges.

        :param user: `Union[int, User]`
            The user ID or User object of the member to be promoted.

        :param is_anonymous: `bool`
            (Optional) Pass True if the promoted administrator's actions should be shown as anonymous in the chat.

        :param can_manage_chat: `bool`
            (Optional) Pass True if the administrator can access the chat event log, chat statistics, message statistics
            in channels, see channel members, see anonymous administrators in supergroups, and ignore slow mode.
            Implied by any other administrator privilege.

        :param can_post_messages: `bool`
            (Optional) Pass True if the administrator can create channel posts. (Channels only)

        :param can_edit_messages: `bool`
            (Optional) Pass True if the administrator can edit messages of other users and can pin messages. (Channels only)

        :param can_delete_messages: `bool`
            (Optional) Pass True if the administrator can delete messages of other users.

        :param can_manage_video_chats: `bool`
            (Optional) Pass True if the administrator can manage video chats.

        :param can_restrict_members: `bool`
            (Optional) Pass True if the administrator can restrict, ban, or unban chat members.

        :param can_promote_members: `bool`
            (Optional) Pass True if the administrator can add new administrators with a subset of their own privileges or
            demote administrators that they have promoted,
            directly or indirectly (promoted by administrators that were appointed by them).

        :param can_change_info: `bool`
            (Optional) Pass True if the administrator can change chat title, photo, and other settings.

        :param can_invite_users: `bool`
            (Optional) Pass True if the administrator can invite new users to the chat.

        :param can_pin_messages: `bool`
            (Optional) Pass True if the administrator can pin messages. (Supergroups only)

        :param can_manage_topics: `bool`
            (Optional) Pass True if the user is allowed to create, rename, close, and reopen forum topics. (Supergroups only)

        :return: `bool`
            Returns True if the member was successfully promoted

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.PROMOTE_CHAT_MEMBER, data={
            'chat_id': self.id,
            'user_id': user if isinstance(user, int) else user.id,
            **exclude_from_dict(locals(), 'user', 'self')
        })

        return bool(data['result'])

    async def set_administrator_custom_title(self, user: Union[int, User], custom_title: str) -> bool:
        """
        Set a custom title for an administrator in a supergroup promoted by the bot

        :param user: `type`
            The user ID or User object of the member to be promoted.

        :param custom_title: `type`
            New custom title for the administrator; 0-16 characters, emoji are not allowed

        :return: `bool`
            Returns True on success

        :raises:
            :raise ValueError: if custom_title is longer than 16 characters
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        if len(custom_title) > 16:
            raise ValueError("New custom title for the administrator must be less than 16 characters long")

        response, data = await method_request("post", APIMethod.SET_CHAT_ADMIN_CUSTOM_TITLE, data={
            'chat_id': self.id,
            'user_id': user if isinstance(user, int) else user.id,
            **exclude_from_dict(locals(), 'user', 'self')
        })

        return bool(data['result'])

    async def ban_sender_chat(self, sender_chat: Union[int, 'Chat']) -> bool:
        """
        Bans a channel chat in a supergroup or a channel.
        Until the chat is unbanned, the owner of the banned chat won't be able to send
        messages on behalf of their channels. The bot must be an administrator in the supergroup
        or channel for this to work and must have the appropriate administrator rights

        :param sender_chat: `Union[int, 'Chat']`
            The sender_chat ID or Chat object of the chat to be banned.

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.BAN_CHAT_SENDER_CHAT, data={
            'chat_id': self.id,
            'sender_chat_id': sender_chat if isinstance(sender_chat, int) else sender_chat.id,
            **exclude_from_dict(locals(), 'sender_chat', 'self')
        })

        return bool(data['result'])

    async def unban_sender_chat(self, sender_chat: Union[int, 'Chat']) -> bool:
        """
        Unbans a previously banned channel chat in a supergroup or channel.
        The bot must be an administrator for this to work and must have the appropriate administrator rights.

        :param sender_chat: `Union[int, 'Chat']`
            The sender_chat ID or Chat object of the chat to be unbanned.

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.UNBAN_CHAT_SENDER_CHAT, data={
            'chat_id': self.id,
            'sender_chat_id': sender_chat if isinstance(sender_chat, int) else sender_chat.id,
            **exclude_from_dict(locals(), 'sender_chat', 'self')
        })

        return bool(data['result'])

    async def set_default_permissions(self,
                                      permissions: ChatPermissions,
                                      use_independent_chat_permissions: bool = None) -> bool:
        """
        Set default chat permissions for all members.
        The bot must be an administrator in the group or a supergroup for this
        to work and must have the can_restrict_members administrator rights.

        :param permissions: `ChatPermissions`
            New default chat permissions

        :param use_independent_chat_permissions: `bool`
            Pass True if chat permissions are set independently.
            Otherwise, the can_send_other_messages and can_add_web_page_previews permissions
            will imply the can_send_messages, can_send_audios, can_send_documents,
            can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions;
            the can_send_polls permission will imply the can_send_messages permission.

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.SET_CHAT_PERMISSIONS, data={
            'chat_id': self.id,
            'permissions': ChatPermissionsSerializer().serialize(obj=permissions),
            'use_independent_chat_permissions': use_independent_chat_permissions,
            **exclude_from_dict(locals(), 'permissions', 'self')
        })

        return bool(data['result'])

    async def export_invite_link(self) -> str:
        """
        Generates a new primary invite link for a chat; any previously generated primary link is revoked.
        The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights.

        :return: `str`
            New invite link

        Notes:
         - Each administrator in a chat generates their own invite links.
         Bots can't use invite links generated by other administrators.
         If you want your bot to work with invite links, it will need to generate its own link
         using exportChatInviteLink or by calling the getChat method.
         If your bot needs to generate a new primary invite link replacing its previous one, use exportChatInviteLink again.

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.EXPORT_CHAT_INVITE_LINK, data={
            'chat_id': self.id,
        })

        return str(data['result'])

    async def create_invite_link(self,
                                 name: str = None,
                                 expire_date: datetime = None,
                                 member_limit: int = None,
                                 creates_join_request: bool = None) -> ChatInviteLink:
        """
        Creates an additional invite link for a chat.
        The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights.
        The link can be revoked using the method revokeChatInviteLink.

        :param name: `str`
            Invite link name; 0-32 characters

        :param expire_date: `datetime`
            Point in time when the link will expire

        :param member_limit: `int`
            The maximum number of users that can be members of the chat
            simultaneously after joining the chat via this invite link; 1-99999

        :param creates_join_request: `bool`
            True, if users joining the chat via the link need to be approved by chat administrators.
            If True, member_limit can't be specified

        :return: `ChatInviteLink`
            New invite link

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        response, data = await method_request("post", APIMethod.CREATE_CHAT_INVITE_LINK, data={
            'chat_id': self.id,
            'name': name,
            'expire_date': expire_date.timestamp(),
            'member_limit': member_limit,
            'creates_join_request': creates_join_request
        })

        return ChatInviteLinkSerializer().serialize(data=data)

    async def send_action(self, action: ChatAction, message_thread_id: int = None) -> bool:
        """
        Sends a chat action to indicate the current status of the bot in the chat.

        :param action: `ChatAction`
            The type of chat action to send, indicating the current status or action.
        :param message_thread_id: `int`
            (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

        :return: `bool`
            Returns True if the action was successfully sent

        Notes:
         - Status is shown for 5 seconds or less (when a message arrives from your bot,
         Telegram clients clear its typing status)

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
        Alias for the teleapi.generics.http.methods.messages.send.send_message
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
        Alias for the teleapi.generics.http.methods.messages.send.send_photo
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
        Alias for the teleapi.generics.http.methods.messages.send.send_audio
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
        Alias for the teleapi.generics.http.methods.messages.send.send_document
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
        Alias for the teleapi.generics.http.methods.messages.send.send_video
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
        Alias for the teleapi.generics.http.methods.messages.send.send_video_note
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
        Alias for the teleapi.generics.http.methods.messages.send.send_poll
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_poll(**payload)

    async def send_contact(self,
                           contact: 'Contact',
                           disable_notification: bool = None,
                           protect_content: bool = None,
                           reply_to_message: Union[int, 'Message'] = None,
                           allow_sending_without_reply: bool = None,
                           reply_markup: Union[
                               'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                           view: 'BaseInlineView' = None
                           ) -> 'Message':
        """
        Alias for the teleapi.generics.http.methods.messages.send.send_contact
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_contact(**payload)

    async def send_dice(self,
                        emoji: 'str' = None,
                        disable_notification: bool = None,
                        protect_content: bool = None,
                        reply_to_message: Union[int, 'Message'] = None,
                        allow_sending_without_reply: bool = None,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None
                        ) -> 'Message':
        """
        Alias for the teleapi.generics.http.methods.messages.send.send_dice
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_dice(**payload)

    async def send_media_group(self,
                               media: List[
                                   Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
                               disable_notification: bool = None,
                               protect_content: bool = None,
                               reply_to_message: Union[int, 'Message'] = None,
                               allow_sending_without_reply: bool = None,
                               reply_markup: Union[
                                   'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                               view: 'BaseInlineView' = None
                               ) -> List['Message']:
        """
        Alias for the teleapi.generics.http.methods.messages.send.send_media_group
        """

        payload = exclude_from_dict(locals(), 'self', 'reply_to_message')
        payload['reply_to_message_id'] = reply_to_message if isinstance(reply_to_message,
                                                                        int) or reply_to_message is None else reply_to_message.id
        payload['chat_id'] = self.id

        return await send_media_group(**payload)

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
        Alias for the teleapi.generics.http.methods.messages.edit.edit_message_text
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
        Alias for the teleapi.generics.http.methods.messages.forward.copy_message
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
        Alias for the teleapi.generics.http.methods.messages.forward.forward_message
        """

        payload = exclude_from_dict(locals(), 'self', 'to_chat', 'message', 'reply_to_message')
        payload['to_chat_id'] = to_chat.id if isinstance(to_chat, Chat) else to_chat
        payload['message_id'] = message if isinstance(message, int) else message.id
        payload['chat_id'] = self.id
        return await forward_message(**payload)
