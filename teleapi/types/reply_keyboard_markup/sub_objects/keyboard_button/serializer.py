from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import KeyboardButton


class KeyboardButtonSerializer(ModelSerializer):
    # request_user
    # request_chat
    # request_poll
    # web_app

    class Meta:
        model = KeyboardButton
