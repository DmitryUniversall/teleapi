from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField, \
    ListSerializerField, EnumSerializerField
from .obj import InputMedia
from ..message_entity import MessageEntitySerializer
from teleapi.enums.parse_mode import ParseMode


class InputMediaSerializer(ModelSerializer):
    type_ = StringSerializerField(read_name='type')
    caption_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    parse_mode = EnumSerializerField(ParseMode, StringSerializerField())

    class Meta:
        model = InputMedia
