from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ChatLocation


class ChatLocationSerializer(ModelSerializer):
    class Meta:
        model = ChatLocation
