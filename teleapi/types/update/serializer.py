from teleapi.core.orm.serializers.generics.fields import IntegerSerializerField, RelatedSerializerField
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.types.message.serializer import MessageSerializer
from .obj import Update
from teleapi.types.callback_query import CallbackQuerySerializer
from teleapi.types.chat_member_updated import ChatMemberUpdatedSerializer


class UpdateSerializer(ModelSerializer):
    id = IntegerSerializerField(read_name="update_id")
    message = RelatedSerializerField(MessageSerializer(), is_required=False)
    edited_message = RelatedSerializerField(MessageSerializer(), is_required=False)
    channel_post = RelatedSerializerField(MessageSerializer(), is_required=False)
    edited_channel_post = RelatedSerializerField(MessageSerializer(), is_required=False)
    callback_query = RelatedSerializerField(CallbackQuerySerializer(), is_required=False)
    bot_chat_member = RelatedSerializerField(ChatMemberUpdatedSerializer(), read_name='my_chat_member', is_required=False)
    chat_member = RelatedSerializerField(ChatMemberUpdatedSerializer(), is_required=False)

    class Meta:
        model = Update
