from .model import ChatMemberRestrictedModel
from teleapi.types.chat_member import ChatMember


class ChatMemberRestricted(ChatMemberRestrictedModel, ChatMember):
    pass
