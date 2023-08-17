from teleapi.core.orm.validators.abc import Validateable
from teleapi.core.orm.typing import JsonValue
from .sized import SizedValidator


class ListValidator(SizedValidator):
    def __init__(self, validator: 'Validateable', **kwargs) -> None:
        super().__init__(**kwargs)
        self.validator = validator

    def validate(self, value: JsonValue) -> JsonValue:
        value = super().validate(value)
        if value is None:
            return

        return [self.validator.validate(element) for element in value]
