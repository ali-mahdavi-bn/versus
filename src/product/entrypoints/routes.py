from fastapi import APIRouter, Request

from backbone.helpers.utils import parse_query_params
from product.bootstrap import bootstrap
from product.domain import commands
from product.domain.commands import GetProduct
from product.service_layer.query.view.get_product import get_product_view
from product.service_layer.query.view.search_product import search_product_view

router = APIRouter(prefix="/api/shop/products", tags=["account"])
bus = bootstrap()


@router.get("/{language:int}/search/")
def search_products(language: int, request: Request):
    params, category_id, limit_, page_ = parse_query_params(request.query_params.multi_items())
    command = commands.SearchProducts(filters=params, category_id=category_id, language=language, limit=limit_,
                                      page=page_)
    print(category_id)
    return search_product_view(command)

# @router.get("/{language:str}/product/")
# def get_product(language: str, product_id: int):
    # command = commands.GetProduct(product_id=product_id, language=language)
    # return get_product_view(command)


@router.get("/{language:str}/{product_slug:str}")
def get_product(language: str, product_slug: str):
    return get_product_view(product_slug=product_slug, language=language)


@router.get("/{language:str}/{product_slug:str}/{category_tag_name:str}")
def get_product_category_tag_name(language: str, product_slug: str, category_tag_name: str):
    # dto = GetProduct(product_slug=product_slug, language=language)
    return get_product_view(product_slug=category_tag_name,language=language)
