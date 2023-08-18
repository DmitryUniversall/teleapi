from teleapi.core.orm.serializers.abc import Serializable
from teleapi.core.orm.typing import JsonValue
from .related import RelatedSerializerField
from teleapi.core.orm.validators.generics.selection import SelectionValidator
from typing import Type, Union
from enum import Enum


class EnumSerializerField(SelectionValidator, RelatedSerializerField):
    def __init__(self, enum_: Type[Enum], serializable: Union[Serializable, str], **kwargs) -> None:
        super().__init__(**kwargs, variations=[field.value for field in list(enum_)], serializable=serializable)
        self.enum_ = enum_

    def to_representation(self, obj: Enum, keep_none_fields: bool = True) -> JsonValue:
        return super().to_representation(obj.value, keep_none_fields=keep_none_fields)
