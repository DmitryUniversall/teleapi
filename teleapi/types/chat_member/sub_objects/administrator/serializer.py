from .obj import ChatAdministrator
from teleapi.types.chat_member import ChatMemberSerializer


class ChatAdministratorSerializer(ChatMemberSerializer):
    class Meta:
        model = ChatAdministrator
