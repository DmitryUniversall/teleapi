from .abc import Validateable
from abc import ABC
from typing import Any
from .exceptions import ValidationError


class BaseValidator(Validateable, ABC):
    def __init__(self, is_required: bool = False, default: Any = None) -> None:
        self.is_required = is_required
        self.default = default

    def validate(self, value: Any) -> Any:
        if value is None and self.default is not None:
            value = self.default
        if value is None and not self.is_required:
            return None
        if value is None and self.is_required:
            raise ValidationError(
                f"Value of Validator {self} is missed"
            )

        return value


class Validator(BaseValidator):
    pass
