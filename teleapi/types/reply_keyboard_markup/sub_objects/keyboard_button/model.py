from typing import Optional

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import (
    StringModelField,
    BooleanModelField
)


class KeyboardButtonModel(Model):
    text: str = StringModelField()
    request_contact: Optional[bool] = BooleanModelField(is_required=False)
    request_location: Optional[bool] = BooleanModelField(is_required=False)

    # request_user
    # request_chat
    # request_poll
    # web_app
