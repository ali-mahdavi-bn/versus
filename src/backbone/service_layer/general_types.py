from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, List, NewType
from uuid import UUID

from pydantic import BaseModel

from backbone.helpers.validation import PhoneNumberValidator


class BaseLanguage(Enum):
    @classmethod
    def members(cls) -> List[BaseLanguage]:
        return [item[1] for item in cls.__members__.items()]


class BaseEnumeration(Enum):
    @classmethod
    def members(cls) -> List[BaseEnumeration]:
        return [item[1] for item in cls.__members__.items()]

    @classmethod
    def find_by_value(cls, value) -> BaseEnumeration:
        for item in cls.members():
            if value == item.value:
                return item


class Command(BaseModel):
    pass


class Dao(BaseModel):
    pass


class Validate(BaseModel):
    pass


class Event(BaseModel):
    pass


class ValueObject(BaseModel):
    pass


class PhoneNumber(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any):
        PhoneNumberValidator("body.phone_number", value).validate()
        return cls


# type table
ID = NewType('ID', int)
Name = NewType('Name', str)
Slug = NewType('Slug', str)
ForeignKeyUuid = NewType('ForeignKeyUuid', UUID)
IsActive = NewType('IsActive', bool)
CreatedAt = NewType('CreatedAt', datetime)
UpdatedAt = NewType('UpdatedAt', datetime)
DeletedAt = NewType('DeletedAt', datetime)

# public
Query = NewType('Query', str)
Params = NewType('Params', dict)
