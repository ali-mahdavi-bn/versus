from uuid import UUID

from backbone.service_layer.general_types import Validate


class GetMaximumAmount(Validate):
    product_slug: str
    category_id: UUID
    language: int
