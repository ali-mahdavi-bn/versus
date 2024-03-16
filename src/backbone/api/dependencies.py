from enum import Enum
from typing import Any

from fastapi.params import Query
from sqlalchemy import desc
from starlette.requests import Request

from backbone.exception import UnauthorizedException, BadRequestException


def current_user(request: Request):
    if request.state.user is None:
        raise UnauthorizedException()
    return request.state.user


class OrderEnum(Enum):
    asc = "asc"
    des = "des"


class OrderByParam:
    def __init__(self, sort_by: str = "id", order: OrderEnum = OrderEnum.asc):
        self.sort_by = sort_by
        self.order = order

    def sql_order_by(self, model: Any):
        if not hasattr(model, self.sort_by):
            raise BadRequestException(f"model has not any attribute {self.sort_by}")

        if self.order == OrderEnum.des.value:
            return desc(getattr(model, self.sort_by))
        else:
            return getattr(model, self.sort_by)



class PaginateParam:
    def __init__(self, offset: int = 0, limit: int = 10, sort_by: str = "id", order="asc"):
        self.offset = offset if offset > 0 else 0
        self.limit = limit if limit <= 100 else 100
        self.sort_by = sort_by
        self.order = order

    def sql_order_by(self, model: Any):
        if not hasattr(model, self.sort_by):
            raise BadRequestException(f"model has not any attribute {self.sort_by}")

        if self.order == OrderEnum.des.value:
            return desc(getattr(model, self.sort_by))
        else:
            return getattr(model, self.sort_by)
