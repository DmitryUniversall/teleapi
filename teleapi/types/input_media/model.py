import os
from typing import Union, List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, ConstantModelField, ListModelField, RelatedModelField
from teleapi.core.utils.files import get_file
from teleapi.core.utils.syntax import default
from teleapi.types.message_entity import MessageEntity
from teleapi.enums.parse_mode import ParseMode


class InputMediaModel(Model):
    type_: str = ConstantModelField("UNKNOWN")
    media: str = StringModelField()
    caption: str = StringModelField()
    caption_entities: List[MessageEntity] = ListModelField(RelatedModelField(MessageEntity))
    parse_mode: ParseMode = RelatedModelField(ParseMode)

    def __init__(self, *, data: Union[str, bytes], filename: str = None, **kwargs) -> None:
        super().__init__(**kwargs)

        data_filename = None
        if isinstance(data, str) and os.path.exists(data):
            data_filename, data = get_file(data)

        filename = default(filename, data_filename)
        if filename is None:
            raise ValueError(f"'filename' for {self.__class__.__name__} was not specified")

        self.media = f"attach://{filename}"
        setattr(self, filename, data)
