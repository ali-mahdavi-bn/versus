from backbone.container.container import Provider, Container
from product.domain.commands import SearchProducts
from product.domain.services.parser_filters import parser_filters
from unit_of_work import UnitOfWork


def search_product_view(command: SearchProducts, uow: UnitOfWork = Provider[Container.uow]):
    filters = command.filters

    with uow:
        if command.category_id:
            filter_clauses, values, values_int, category = parser_filters(filters)
            products = uow.product.search_product(filter_clauses=filter_clauses, category=category,
                                                  language=command.language, values=values,
                                                  values_int=values_int, limit=command.limit,
                                                  offset=command.page)
            faced = uow.category.get_attributes_category(command.category_id,
                                                         attribute_id=filter_clauses)

            return {
                'products': products if products and (products[0]).get('product_id') else None,
                'faces': faced
            }

        else:
            faced = uow.category.get_all_category()
            products = uow.product.others_products()
            return {
                'products': products,
                'faces': faced
            }
