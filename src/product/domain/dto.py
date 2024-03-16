from backbone.service_layer.general_types import Dto


class GetProduct(Dto):
    product_slug: str
    language: int
