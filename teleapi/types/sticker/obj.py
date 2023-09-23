from .model import StickerModel
from teleapi.types.filelike import Filelike


class Sticker(StickerModel, Filelike):
    pass
