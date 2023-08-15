from abc import ABC
from typing import Any, Optional

from teleapi.core.orm.field import Field
from teleapi.core.orm.validators.validator import BaseValidator


class BaseModelField(BaseValidator, Field, ABC):
    def __set__(self, instance: Any, value: Any) -> None:
        validated = self.validate(value)
        instance.__dict__[self.__attribute_name__] = validated

    def __get__(self, instance: Optional[Any] = None, owner: Optional[type] = None) -> Any:
        try:
            if instance is not None:
                return instance.__dict__[self.__attribute_name__]
            return owner.__dict__[self.__attribute_name__]
        except KeyError:
            return self


class ModelField(BaseModelField):
    pass
