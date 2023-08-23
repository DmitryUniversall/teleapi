from teleapi.core.orm.serializers.generics.fields import (
    StringSerializerField,
    RelatedSerializerField,
    ListSerializerField,
    EnumSerializerField
)
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Chat
from .chat_type import ChatType


class ChatSerializer(ModelSerializer):
    type_ = EnumSerializerField(ChatType, StringSerializerField(), read_name="type")
    active_usernames = ListSerializerField(StringSerializerField(), is_required=False, default=[])
    pinned_message = RelatedSerializerField('MessageSerializer', is_required=False)

    # location = RelatedValidator(ChatLocation, is_required=False)
    # permissions = RelatedValidator(ChatPermissions, is_required=False)
    # photo = RelatedValidator(ChatPhoto)

    class Meta:
        model = Chat
