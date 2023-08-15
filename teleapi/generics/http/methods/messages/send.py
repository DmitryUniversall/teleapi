import os
from typing import TYPE_CHECKING, List
from typing import Union

from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.http.request.api_request import method_request
from teleapi.core.utils.collections import clear_none_values, exclude_from_dict
from teleapi.core.utils.files import get_file
from teleapi.generics.http.methods.utils import make_data_form
from teleapi.enums.parse_mode import ParseMode
from .utils import get_converted_reply_markup

if TYPE_CHECKING:
    from teleapi.types.message import Message
    from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from teleapi.core.ui.inline_view.view import BaseInlineView
    from teleapi.types.forece_reply import ForceReply
    from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
    from teleapi.types.message_entity import MessageEntity
    from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup


async def send_message(chat_id: Union[int, str],
                       text: str,
                       reply_to_message_id: int = None,
                       message_thread_id: int = None,
                       parse_mode: ParseMode = ParseMode.NONE,
                       disable_web_page_preview: bool = None,
                       disable_notification: bool = None,
                       protect_content: bool = None,
                       allow_sending_without_reply: bool = None,
                       reply_markup: Union[
                           'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                       entities: List['MessageEntity'] = None,
                       view: 'BaseInlineView' = None
                       ) -> 'Message':
    """
    Sends a text message to a specified chat

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param text: `str`
        The text of the message to be sent.

    :param reply_to_message_id: `int`
        (Optional) If the message is a reply, the ID of the original message.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the message text.
        Default is `ParseMode.NONE`.

    :param disable_web_page_preview: `bool`
        (Optional) Disable web page previews for links in the message.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param protect_content: `bool`
        (Optional) Mark the message as protected content.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param entities: `List['MessageEntity']`
        (Optional) List of special entities that appear in the message text.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control message interface.

    :return: `Message`
        The sent message.

    :raises:
        :raise: ApiRequestError or any of its subclasses if request sent to the Telegram Bot API failed
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = clear_none_values(exclude_from_dict(locals(), 'view'))

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_MESSAGE, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message


async def send_photo(chat_id: Union[int, str],
                     photo: Union[bytes, str],
                     message_thread_id: int = None,
                     caption: str = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     has_spoiler: bool = None,
                     disable_notification: bool = None,
                     protect_content: bool = None,
                     reply_to_message_id: int = None,
                     allow_sending_without_reply: bool = None,
                     reply_markup: Union[
                         'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                     view: 'BaseInlineView' = None,
                     filename: str = None,
                     ) -> 'Message':
    """
    Sends a photo to a specified chat

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param photo: `Union[bytes, str]`
        The photo file to be sent. It can be provided as bytes, a file path (str), or the file_id of a photo file that
        already exists on the Telegram servers (str).

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the photo.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param has_spoiler: `bool`
        (Optional) Mark the photo as containing spoilers.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param protect_content: `bool`
        (Optional) Mark the message content as protected.

    :param reply_to_message_id: `int`
        (Optional) If the photo is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control message interface.

    :param filename: `str`
        (Optional) The filename to be used when sending the photo.

    :return: `Message`
        The sent message.

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API sent fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """

    if isinstance(photo, str) and os.path.exists(photo):
        filename, photo = get_file(photo)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(clear_none_values(exclude_from_dict(locals(), 'view', 'filename', 'photo')))

    request_data.add_field('photo', photo, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_PHOTO, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message


async def send_audio(chat_id: Union[int, str],
                     audio: Union[bytes, str],
                     message_thread_id: int = None,
                     caption: str = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     duration: int = None,
                     performer: str = None,
                     title: str = None,
                     thumbnail: Union[bytes, str] = None,
                     disable_notification: bool = None,
                     protect_content: bool = None,
                     reply_to_message_id: int = None,
                     allow_sending_without_reply: bool = None,
                     reply_markup: Union[
                         'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                     view: 'BaseInlineView' = None,
                     filename: str = None
                     ) -> 'Message':
    """
    Sends an audio file to a specified chat

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param audio: `Union[bytes, str]`
        The audio file to be sent. It can be provided as bytes, a file path (str), or the file_id of an audio file that
        already exists on the Telegram servers.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the audio.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param duration: `int`
        (Optional) Duration of the audio in seconds.

    :param performer: `str`
        (Optional) Performer of the audio.

    :param title: `str`
        (Optional) Title of the audio.

    :param thumbnail: `Union[bytes, str]`
        (Optional) Thumbnail of the audio, can be provided as bytes or a file path.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param protect_content: `bool`
        (Optional) Mark the message content as protected.

    :param reply_to_message_id: `int`
        (Optional) If the audio is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :param filename: `str`
        (Optional) The filename to be used when sending the audio.

    :return: The sent message.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320.
    """

    if isinstance(audio, str) and os.path.exists(audio):
        filename, audio = get_file(audio)
    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(
        clear_none_values(exclude_from_dict(locals(), 'view', 'audio', 'filename', 'thumbnail')))

    if thumbnail:
        request_data.add_field('thumbnail', thumbnail)
    request_data.add_field('audio', audio, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_AUDIO, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message


async def send_document(chat_id: Union[int, str],
                        document: Union[bytes, str],
                        message_thread_id: int = None,
                        caption: str = None,
                        parse_mode: ParseMode = ParseMode.NONE,
                        caption_entities: List['MessageEntity'] = None,
                        disable_content_type_detection: bool = None,
                        thumbnail: Union[bytes, str] = None,
                        disable_notification: bool = None,
                        protect_content: bool = None,
                        reply_to_message_id: int = None,
                        allow_sending_without_reply: bool = None,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None,
                        filename: str = None
                        ) -> 'Message':
    """
    Sends a document file to a specified chat.

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param document: `Union[bytes, str]`
        The document file to be sent. It can be provided as bytes, a file path (str), or the file_id of a document file
        that already exists on the Telegram servers.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the document.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param disable_content_type_detection: `bool`
        (Optional) Disables automatic content type detection for the document.

    :param thumbnail: `Union[bytes, str]`
        (Optional) Thumbnail of the document, can be provided as bytes or a file path.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param protect_content: `bool`
        (Optional) Mark the message content as protected.

    :param reply_to_message_id: `int`
        (Optional) If the document is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :param filename: `str`
        (Optional) The filename to be used when sending the document.

    :return: The sent message object.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320.
    """

    if isinstance(document, str) and os.path.exists(document):
        filename, document = get_file(document)
    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(
        clear_none_values(exclude_from_dict(locals(), 'view', 'document', 'filename', 'thumbnail')))

    if thumbnail:
        request_data.add_field('thumbnail', thumbnail)
    request_data.add_field('document', document, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_DOCUMENT, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message


async def send_video(chat_id: Union[int, str],
                     video: Union[bytes, str],
                     thumbnail: Union[bytes, str],
                     message_thread_id: int = None,
                     caption: str = None,
                     duration: int = None,
                     height: int = None,
                     width: int = None,
                     has_spoiler: bool = None,
                     supports_streaming: bool = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     disable_notification: bool = None,
                     reply_to_message_id: int = None,
                     allow_sending_without_reply: bool = None,
                     reply_markup: Union[
                         'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                     view: 'BaseInlineView' = None,
                     filename: str = None,
                     ) -> 'Message':
    """
    Sends a video to a specified chat.

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param video: `Union[bytes, str]`
        The video to be sent. It can be provided as bytes, a file path (str), or the file_id of a video file
        that already exists on the Telegram servers.

    :param thumbnail: `Union[bytes, str]`
        The thumbnail of the video. It should be provided as bytes or a file path.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the video.

    :param duration: `int`
        (Optional) Duration of the video in seconds.

    :param height: `int`
        (Optional) Height of the video in pixels.

    :param width: `int`
        (Optional) Width of the video in pixels.

    :param has_spoiler: `bool`
        (Optional) Mark the video as containing spoilers.

    :param supports_streaming: `bool`
        (Optional) If True, the video supports streaming.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param reply_to_message_id: `int`
        (Optional) If the video is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :param filename: `str`
        (Optional) The filename to be used when sending the video.

    :return: The sent message object.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320.
    """

    if isinstance(video, str) and os.path.exists(video):
        filename, video = get_file(video)
    if isinstance(thumbnail, str) and os.path.exists(video):
        _, thumbnail = get_file(thumbnail)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(
        clear_none_values(exclude_from_dict(locals(), 'view', 'video', 'filename', 'thumbnail')))

    if thumbnail:
        request_data.add_field('thumbnail', thumbnail)
    request_data.add_field('video', video, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_VIDEO, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message


async def send_animation(chat_id: Union[int, str],
                         animation: Union[bytes, str],
                         thumbnail: Union[bytes, str],
                         message_thread_id: int = None,
                         caption: str = None,
                         duration: int = None,
                         width: int = None,
                         height: int = None,
                         has_spoiler: bool = None,
                         protect_content: bool = None,
                         parse_mode: ParseMode = ParseMode.NONE,
                         caption_entities: List['MessageEntity'] = None,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         allow_sending_without_reply: bool = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         filename: str = None,
                         view: 'BaseInlineView' = None
                         ) -> 'Message':
    """
    Sends an animation to a specified chat.

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param animation: `Union[bytes, str]`
        The animation to be sent. It can be provided as bytes, a file path (str), or the file_id of an animation file
        that already exists on the Telegram servers.

    :param thumbnail: `Union[bytes, str]`
        The thumbnail of the animation. It should be provided as bytes or a file path.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the animation.

    :param duration: `int`
        (Optional) Duration of the animation in seconds.

    :param width: `int`
        (Optional) Width of the animation in pixels.

    :param height: `int`
        (Optional) Height of the animation in pixels.

    :param has_spoiler: `bool`
        (Optional) Mark the animation as containing spoilers.

    :param protect_content: `bool`
        (Optional) Mark the message content as protected.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param reply_to_message_id: `int`
        (Optional) If the animation is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param filename: `str`
        (Optional) The filename to be used when sending the animation.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :return: The sent message object.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320.
    """

    if isinstance(animation, str) and os.path.exists(animation):
        filename, animation = get_file(animation)
    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(
        clear_none_values(exclude_from_dict(locals(), 'view', 'animation', 'filename', 'thumbnail')))

    if thumbnail:
        request_data.add_field('thumbnail', thumbnail)
    request_data.add_field('animation', animation, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_ANIMATION, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    return message


async def send_voice(chat_id: Union[int, str],
                     voice: Union[bytes, str],
                     message_thread_id: int = None,
                     caption: str = None,
                     duration: int = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     disable_notification: bool = None,
                     reply_to_message_id: int = None,
                     allow_sending_without_reply: bool = None,
                     reply_markup: Union[
                         'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                     filename: str = None,
                     view: 'BaseInlineView' = None
                     ) -> 'Message':
    """
    Sends a voice message to a specified chat

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param voice: `Union[bytes, str]`
        The voice message to be sent. It can be provided as bytes, a file path (str), or the file_id of a voice message
        that already exists on the Telegram servers.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param caption: `str`
        (Optional) A caption to accompany the voice message.

    :param duration: `int`
        (Optional) Duration of the voice message in seconds.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param reply_to_message_id: `int`
        (Optional) If the voice message is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param filename: `str`
        (Optional) The filename to be used when sending the voice message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :return: The sent message object.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """
    if isinstance(voice, str) and os.path.exists(voice):
        filename, voice = get_file(voice)

    parse_mode = parse_mode.value
    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(clear_none_values(exclude_from_dict(locals(), 'view', 'filename', 'voice')))

    request_data.add_field('voice', voice, filename=filename)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_VOICE, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    return message


async def send_video_note(chat_id: Union[int, str],
                          video_note: Union[bytes, str],
                          message_thread_id: int = None,
                          duration: int = None,
                          length: int = None,
                          protect_content: bool = None,
                          disable_notification: bool = None,
                          reply_to_message_id: int = None,
                          allow_sending_without_reply: bool = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                          view: 'BaseInlineView' = None
                          ) -> 'Message':
    """
    Sends a video note (short video message) to a specified chat.

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param video_note: `Union[bytes, str]`
        The video note to be sent. It can be provided as bytes, a file path (str), or the file_id of a video note
        that already exists on the Telegram servers.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param duration: `int`
        (Optional) Duration of the video note in seconds.

    :param length: `int`
        (Optional) Length of the video note in bytes.

    :param protect_content: `bool`
        (Optional) Mark the message content as protected.

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param reply_to_message_id: `int`
        (Optional) If the video note is a reply, the ID of the original message.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control the message interface.

    :return: The sent message object.
    :rtype: `Message`

    :raises:
        :raise: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
    """

    if isinstance(video_note, str) and os.path.exists(video_note):
        filename, video_note = get_file(video_note)

    reply_markup = await get_converted_reply_markup(reply_markup, view)
    request_data = make_data_form(clear_none_values(exclude_from_dict(locals(), 'view', 'video_note')))

    request_data.add_field('video_note', video_note)

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", APIMethod.SEND_VIDEO_NOTE, data=request_data)
    message = MessageSerializer().serialize(data=data['result'])

    return message
