from typing import TYPE_CHECKING
from typing import Union
from teleapi.core.http.request.api_request import method_request
from teleapi.core.utils.collections import clear_none_values
from .utils import get_converted_reply_markup
from teleapi.types.forece_reply import ForceReply
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup
from teleapi.core.http.request.api_method import APIMethod

if TYPE_CHECKING:
    from teleapi.types.message import Message
    from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from teleapi.core.ui.inline_view.view import BaseInlineView


async def edit_message_text(chat_id: Union[int, str],
                            text: str,
                            message_id: int,
                            inline_message_id: int = None,
                            parse_mode: ParseMode = ParseMode.NONE,
                            view: 'BaseInlineView' = None,
                            disable_web_page_preview: bool = None,
                            reply_markup: Union[
                                'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                            entities=None,
                            ) -> Union['Message', bool]:
    from teleapi.types.message.serializer import MessageSerializer

    reply_markup = await get_converted_reply_markup(reply_markup, view)

    request_data = clear_none_values({
        "chat_id": chat_id,
        "text": text,
        "message_id": message_id,
        "inline_message_id": inline_message_id,
        "parse_mode": parse_mode.value,
        "disable_web_page_preview": disable_web_page_preview,
        "reply_markup": reply_markup,
        "entities": entities
    })

    response, data = await method_request("POST", APIMethod.EDIT_MESSAGE_TEXT, data=request_data)

    if data['result'] == 'true':
        return True

    message = MessageSerializer().serialize(data=data['result'])

    if view:
        view.message = message

    return message
