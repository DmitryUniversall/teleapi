from enum import Enum


class ChatAction(Enum):
    TYPING: str = "typing"
    UPLOAD_PHOTO: str = "upload_photo"
    RECORD_VIDEO: str = "record_video"
    RECORD_VOICE: str = "record_voice"
    UPLOAD_VOICE: str = "upload_voice"
    UPLOAD_DOCUMENT: str = "upload_document"
    CHOOSE_STICKER: str = "choose_sticker"
    FIND_LOCATION: str = "find_location"
    RECORD_VIDEO_NOTE: str = "record_video_note"
    UPLOAD_VIDEO_NOTE: str = "upload_video_note"
