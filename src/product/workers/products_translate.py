from typing import List

from backbone.container.container import Provider, Container
from backbone.helpers.translator import Translator
# from backbone.helpers.translator import Translator
from mapper import mapper_init
from product.domain.entities import Language, ProductTranslate
from unit_of_work import UnitOfWork

mapper_init()


def _translate_products(uow, languages, translator: Translator = Provider[Container.translator]):
    translate_products: List[ProductTranslate] = uow.translate_product.orm \
        .filter(ProductTranslate.language == 2).all()

    new_translate_products = []
    languages_id = [i.id for i in languages]
    for translate_product in translate_products:
        if translate_product.language in languages_id:
            for language in languages:
                if translate_product.language == language.id:
                    continue
                name = translator.translate(translate_product.name, language=language.name)
                description = translator.translate(translate_product.description, language=language.name)
                new_translate_product = ProductTranslate.create(
                    name=name,
                    language=language.id,
                    product_id=translate_product.product_id,
                    description=description
                )
                new_translate_products.append(new_translate_product)
    return new_translate_products


def products_translate_worker():
    uow = UnitOfWork()
    with uow:
        languages: List[Language] = uow.language.orm.all()
    while True:
        with uow:
            if categories := _translate_products(uow, languages):
                uow.session.bulk_save_objects(categories)
                uow.commit()

