from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import InlineKeyboardButton
from teleapi.types.web_app_info import WebAppInfoSerializer
from teleapi.types.login_url import LoginUrlSerializer
from teleapi.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChatSerializer
from teleapi.types.callback_game import CallbackGameSerializer


class InlineKeyboardButtonSerializer(ModelSerializer):
    web_app = RelatedSerializerField(WebAppInfoSerializer())
    login_url = RelatedSerializerField(LoginUrlSerializer())
    switch_inline_query_chosen_chat = RelatedSerializerField(SwitchInlineQueryChosenChatSerializer())
    callback_game = RelatedSerializerField(CallbackGameSerializer())

    class Meta:
        model = InlineKeyboardButton
