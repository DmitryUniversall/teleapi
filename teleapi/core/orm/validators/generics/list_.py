from teleapi.core.orm.validators.validator import Validator
from teleapi.core.orm.validators.abc import Validateable
from teleapi.core.orm.typing import JsonValue


class ListValidator(Validator):
    def __init__(self, validator: 'Validateable', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.validator = validator

    def validate(self, value: JsonValue) -> JsonValue:
        value = super().validate(value)
        if value is None:
            return

        return [self.validator.validate(element) for element in value]
