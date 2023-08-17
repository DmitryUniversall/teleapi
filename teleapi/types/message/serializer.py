from teleapi.core.orm.serializers.generics.fields import (
    IntegerSerializerField,
    RelatedSerializerField,
    ListSerializerField
)
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.types.chat.serializer import ChatSerializer
from teleapi.types.user.serializer import UserSerializer
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkupSerializer
from .obj import Message
from teleapi.types.message_entity import MessageEntitySerializer
from ..animation.serializer import AnimationSerializer
from ..audio.serializer import AudioSerializer
from ..contact import ContactSerializer
from ..document import DocumentSerializer
from ..photo_size.serializer import PhotoSizeSerializer
from ..poll import PollSerializer
from ..video.serializer import VideoSerializer
from ..video_note import VideoNoteSerializer
from ..voice.serializer import VoiceSerializer


class MessageSerializer(ModelSerializer):
    id = IntegerSerializerField(read_name="message_id")
    author = RelatedSerializerField(UserSerializer(), read_name="from", is_required=False)
    chat = RelatedSerializerField(ChatSerializer())
    thread_id = IntegerSerializerField(read_name="message_thread_id", is_required=False)
    sender_chat = RelatedSerializerField(ChatSerializer(), is_required=False)
    via_bot = RelatedSerializerField(UserSerializer(), is_required=False)
    reply_markup = RelatedSerializerField(InlineKeyboardMarkupSerializer(), is_required=False)
    forward_from = RelatedSerializerField(UserSerializer(), is_required=False)
    forward_from_chat = RelatedSerializerField(ChatSerializer(), is_required=False)
    reply_to_message = RelatedSerializerField('MessageSerializer', is_required=False)
    pinned_message = RelatedSerializerField('MessageSerializer', is_required=False)
    entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    caption_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    photo = ListSerializerField(RelatedSerializerField(PhotoSizeSerializer()), is_required=False)
    animation = RelatedSerializerField(AnimationSerializer(), is_required=False)
    audio = RelatedSerializerField(AudioSerializer(), is_required=False)
    document = RelatedSerializerField(DocumentSerializer(), is_required=False)
    video = RelatedSerializerField(VideoSerializer(), is_required=False)
    video_note = RelatedSerializerField(VideoNoteSerializer(), is_required=False)
    voice = RelatedSerializerField(VoiceSerializer(), is_required=False)
    new_chat_photo = ListSerializerField(RelatedSerializerField(PhotoSizeSerializer()), is_required=False)
    new_chat_members = ListSerializerField(RelatedSerializerField(UserSerializer()), is_required=False)
    left_chat_member = RelatedSerializerField(UserSerializer(), is_required=False)
    contact = RelatedSerializerField(ContactSerializer(), is_required=False)
    poll = RelatedSerializerField(PollSerializer(), is_required=False)

    class Meta:
        model = Message
