from .obj import ChatMemberRestricted
from teleapi.types.chat_member import ChatMemberSerializer


class ChatMemberRestrictedSerializer(ChatMemberSerializer):
    class Meta:
        model = ChatMemberRestricted
