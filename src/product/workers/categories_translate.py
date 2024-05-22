import time
from typing import List

from backbone.helpers.translator import Translator
from backbone.infrastructure.log.logger import Logger
from mapper import mapper_init
from product.domain.entities.attribute.attribute_translate import AttributeTranslate
from product.domain.language import Language
from unit_of_work import UnitOfWork

mapper_init()


def _translate_categories(uow, languages):
    translate_categories: List[AttributeTranslate] = (uow.translate_category.orm.
                                                      filter(AttributeTranslate.language == 2
                                                             )).all()
    new_translate_categories = []
    languages_id = [i.id for i in languages]
    for translate_category in translate_categories:
        if translate_category.language in languages_id:
            for language in languages:
                if translate_category.language == language.id:
                    continue
                name = Translator.translate(translate_category.name, language=language.name)
                show_name = Translator.translate(translate_category.show_name, language=language.name)
                description = Translator.translate(translate_category.description, language=language.name)
                new_translate_category = AttributeTranslate.create(
                    name=name,
                    language=language.id,
                    category_attribute_id=translate_category.category_attribute_id,
                    show_name=show_name,
                    description=description
                )
                new_translate_categories.append(new_translate_category)
    return new_translate_categories


def categories_translate_worker():
    uow = UnitOfWork()
    with uow:
        languages: List[Language] = uow.language.orm.all()
    while True:
        try:
            with uow:
                if categories := _translate_categories(uow, languages):
                    uow.session.bulk_save_objects(categories)
                    uow.commit()
            time.sleep(300)
        except Exception as e:
            Logger.info(e)
            uow.session.rollback()
            uow.session.close()
            time.sleep(300)


