from .model import ChatAdministratorModel
from teleapi.types.chat_member import ChatMember


class ChatAdministrator(ChatAdministratorModel, ChatMember):
    pass
