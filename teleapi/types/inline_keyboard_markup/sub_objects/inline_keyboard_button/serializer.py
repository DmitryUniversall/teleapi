from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import InlineKeyboardButton


class InlineKeyboardButtonSerializer(ModelSerializer):
    # web_app
    # login_url
    # switch_inline_query_chosen_chat
    # callback_game

    class Meta:
        model = InlineKeyboardButton
