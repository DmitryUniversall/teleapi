from teleapi.core.orm.models.generics.fields import BooleanModelField, ConstantModelField
from teleapi.types.input_media import InputMediaModel


class InputMediaDocumentModel(InputMediaModel):
    type_: str = ConstantModelField("document")
    disable_content_type_detection: bool = BooleanModelField(default=False)

    def __init__(self, *, thumbnail_data: bytes = None, thumbnail_filename: str = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if thumbnail_data is not None:
            if thumbnail_filename is None:
                raise ValueError('You must define filename for thumbnail')

            self.thumbnail = f"attach://{thumbnail_filename}"
            setattr(self, thumbnail_filename, thumbnail_data)
