from typing import Dict, Any

from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField, \
    ListSerializerField, EnumSerializerField
from .obj import InputMedia
from ..message_entity import MessageEntitySerializer
from teleapi.enums.parse_mode import ParseMode
from ...core.orm.typing import JsonValue


class InputMediaSerializer(ModelSerializer):
    __enable_warnings__ = False

    type_ = StringSerializerField(read_name='type')
    caption_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    parse_mode = EnumSerializerField(ParseMode, StringSerializerField(), is_required=False)

    class Meta:
        model = InputMedia
