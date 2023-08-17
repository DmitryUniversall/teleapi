from typing import Any

from .typed import TypedValidator
from teleapi.core.orm.validators.exceptions import ValidationError
from datetime import datetime


class BooleanValidator(TypedValidator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, type_=bool)


class IntegerValidator(TypedValidator):
    def __init__(self, min_value: int = None, max_value: int = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, type_=int)
        if min_value is not None and (not isinstance(min_value, int) or min_value <= 0):
            raise TypeError('min_length must be a positive integer')
        elif min_value is not None and (not isinstance(max_value, int) or max_value <= 0):
            raise TypeError('max_length must be a positive integer')
        elif (min_value is not None and max_value is not None) and max_value < min_value:
            raise ValueError('min_length must be less then max_length')

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> Any:
        value = super().validate(value)

        if value is None:
            return None

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f'Value of validator {self} must be greater than {self.min_value}')
        elif self.max_value is not None and value > self.max_value:
            raise ValidationError(f'Value of validator {self} must be less than {self.max_value}')

        return value


class StringValidator(TypedValidator):
    def __init__(self, min_length: int = None, max_length: int = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, type_=str)

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
            raise ValidationError(f'String length of validator {self} must be greater than {self.min_length}')
        elif self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f'String length of validator {self} must be less than {self.min_length}')

        return value


class DatetimeValidator(TypedValidator):  # TODO: min, max datetime
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, type_=datetime)
