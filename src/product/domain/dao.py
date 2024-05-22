from backbone.service_layer.general_types import Dao


class GetProductDao(Dao):
    product_slug: str
    language: int
