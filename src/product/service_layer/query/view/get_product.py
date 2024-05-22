from backbone.container.container import Provider, Container
from backbone.helpers.utils import cache
from product.domain.services.min_max_avg_value_product import min_max_avg_value_product
from unit_of_work import UnitOfWork


# @cache(ttl=49)
def _get_histogram(attribute_id, uow: UnitOfWork = Provider[Container.uow]):
    with uow:
        try:
            his = uow.product.generate_histogram(attribute_id)
            return his
        except Exception as e:
            print(e)
            return []


# @cache(ttl=49)
def _add_min_max_trend_to_attribute(product, min_max):
    if not product:
        return
    print('b',product.get("attributes"))
    if attributes := product.get("attributes"):
        for attribute in attributes:
            min_attribute = min_max.get(attribute.get("name"), {}).get('min')
            max_attribute = min_max.get(attribute.get("name"), {}).get('max')
            avg_attribute = min_max.get(attribute.get("name"), {}).get('avg')
            attribute['min'] = min_attribute
            attribute['max'] = max_attribute
            attribute['avg'] = avg_attribute
            if max_attribute != min_attribute:
                attribute['trend'] = _get_histogram(attribute.get('ca'))

    return product


def slice_slug(slug):
    slugs = slug.split("-vs-")
    slugs = set(slugs)
    return slugs


# @cache(ttl=49)
def _cache_get_product(product_slug, language, uow: UnitOfWork = Provider[Container.uow]):

    with uow:
        product = uow.product.get_product(product_slug)
        min_max = min_max_avg_value_product(language_id=language)
        product_attribute_have_min_max = _add_min_max_trend_to_attribute(product=product, min_max=min_max)
        print(product)
    print("product")

    return product_attribute_have_min_max


def get_product_view(product_slug: str, language: str):
    slugs = slice_slug(product_slug)
    products = [
        _cache_get_product(slug, language)
        for slug in slugs
    ]

    return products
