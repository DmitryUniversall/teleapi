from typing import Any
from teleapi.core.orm.validators.exceptions import ValidationError
from teleapi.core.orm.validators.validator import Validator


class SizedValidator(Validator):
    def __init__(self, min_length: int = None, max_length: int = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if min_length is not None and (not isinstance(min_length, int) or min_length <= 0):
            raise TypeError('min_length must be a positive integer')
        elif max_length is not None and (not isinstance(max_length, int) or max_length <= 0):
            raise TypeError('max_length must be a positive integer')
        elif (min_length is not None and max_length is not None) and max_length < min_length:
            raise ValueError('min_length must be less then max_length')

        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: Any) -> Any:
        value = super().validate(value)

        if value is None:
            return None

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f'Value length for validator {self} must be greater than {self.min_length}')
        elif self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f'Value length for validator {self} must be less than {self.min_length}')

        return value
