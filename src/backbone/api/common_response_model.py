from typing import Generic, Optional, List, Dict

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel

from typing import TypeVar


M = TypeVar('M')


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Number of items returned in the response')
    data: List[M] = Field(description='List of items returned in the response following given criteria')


class BaseCommandResponse(BaseModel):
    message: Optional[str] = ""
    data: Dict = Field(description='List of items returned in the response following given criteria')
