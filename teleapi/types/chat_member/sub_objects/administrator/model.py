from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, ConstantModelField
from teleapi.types.chat_member import ChatMemberModel
from typing import Optional


class ChatAdministratorModel(ChatMemberModel):
    status: str = ConstantModelField("administrator")
    can_be_edited: bool = BooleanModelField(default=False)
    is_anonymous: bool = BooleanModelField(default=False)
    can_manage_chat: bool = BooleanModelField(default=False)
    can_delete_messages: bool = BooleanModelField(default=False)
    can_manage_video_chats: bool = BooleanModelField(default=False)
    can_restrict_members: bool = BooleanModelField(default=False)
    can_promote_members: bool = BooleanModelField(default=False)
    can_change_info: bool = BooleanModelField(default=False)
    can_invite_users: bool = BooleanModelField(default=False)
    can_post_messages: Optional[bool] = BooleanModelField(is_required=False)
    can_edit_messages: Optional[bool] = BooleanModelField(is_required=False)
    can_pin_messages: Optional[bool] = BooleanModelField(is_required=False)
    can_manage_topics: Optional[bool] = BooleanModelField(is_required=False)
    custom_title: Optional[str] = StringModelField(is_required=False)
