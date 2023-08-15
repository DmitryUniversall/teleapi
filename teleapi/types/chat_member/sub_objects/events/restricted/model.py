from datetime import datetime

from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, ConstantModelField, \
    UnixTimestampModelField
from teleapi.types.chat_member import ChatMemberModel
from typing import Optional


class ChatMemberRestrictedModel(ChatMemberModel):
    status: str = ConstantModelField("restricted")
    is_member: bool = BooleanModelField(default=False)
    can_send_messages: bool = BooleanModelField(default=False)
    can_send_audios: bool = BooleanModelField(default=False)
    can_send_documents: bool = BooleanModelField(default=False)
    can_send_photos: bool = BooleanModelField(default=False)
    can_send_videos: bool = BooleanModelField(default=False)
    can_send_video_notes: bool = BooleanModelField(default=False)
    can_send_voice_notes: bool = BooleanModelField(default=False)
    can_send_polls: bool = BooleanModelField(default=False)
    can_send_other_messages: bool = BooleanModelField(default=False)
    can_add_web_page_previews: bool = BooleanModelField(default=False)
    can_change_info: bool = BooleanModelField(default=False)
    can_invite_users: bool = BooleanModelField(default=False)
    can_pin_messages: Optional[bool] = BooleanModelField(default=False)
    can_manage_topics: Optional[bool] = BooleanModelField(default=False)
    until_date: datetime = UnixTimestampModelField()
