from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.user import UserSerializer
from .obj import PollAnswer


class PollAnswerSerializer(ModelSerializer):
    user = RelatedSerializerField(UserSerializer())

    class Meta:
        model = PollAnswer
