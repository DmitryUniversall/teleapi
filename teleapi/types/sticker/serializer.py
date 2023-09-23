from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField, EnumSerializerField
from .obj import Sticker
from teleapi.types.photo_size import PhotoSizeSerializer
from teleapi.types.file import FileSerializer
from teleapi.types.filelike import FilelikeSerializer
from .sub_objects.sticker_type import StickerType


class StickerSerializer(ModelSerializer, FilelikeSerializer):
    type_ = EnumSerializerField(StickerType, StringSerializerField(), read_name='type')
    thumbnail = RelatedSerializerField(PhotoSizeSerializer(), is_required=False)
    premium_animation = RelatedSerializerField(FileSerializer(), is_required=False)

    class Meta:
        model = Sticker
