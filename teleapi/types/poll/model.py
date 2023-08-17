from typing import Optional, List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, BooleanModelField, \
    RelatedModelField, ListModelField, UnixTimestampModelField
from .sub_object.option import PollOption
from teleapi.types.message_entity import MessageEntity
from datetime import datetime


class PollModel(Model):
    id: str = StringModelField()
    question: str = StringModelField(max_length=300)
    options: List[PollOption] = ListModelField(RelatedModelField(PollOption), min_length=2, max_length=10)
    total_voter_count: int = IntegerModelField()
    is_closed: bool = BooleanModelField(default=False)
    is_anonymous: bool = BooleanModelField(default=False)
    type_: str = StringModelField()
    allows_multiple_answers: bool = BooleanModelField(default=False)
    correct_option_id: Optional[int] = IntegerModelField(is_required=False)
    explanation: Optional[str] = StringModelField(is_required=False, max_length=200)
    explanation_entities: List[MessageEntity] = ListModelField(RelatedModelField(MessageEntity))
    open_period: Optional[int] = IntegerModelField(is_required=False)
    close_date: Optional[datetime] = UnixTimestampModelField(is_required=False)
