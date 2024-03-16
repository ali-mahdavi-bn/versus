from typing import List

from backbone.crawler.exeptions.don_finished_worker import DonFinishedWorkerSpider
from backbone.crawler.helper.helpers.requests import RequestArgs
from backbone.crawler.helper.helpers.response import Response
from backbone.crawler.spider import Spider
from product.domain.entities import Category
from product.spider.utils.clear_data import clear_page_category_verses, CategoryDTO
from unit_of_work import UnitOfWork


class CategoryVersusSpider(Spider):
    name = "versus_spider"

    def start_requests(self, **kwargs):
        url = "https://versus.com/en/categories"
        yield RequestArgs(url=url, callback=self.parse)

    def parse(self, response: Response):
        detail_categories: List[CategoryDTO] = clear_page_category_verses(response)
        categories: List[Category] = []
        result = self._get_categories()
        for detail_category in detail_categories:
            if detail_category.name in result:
                continue

            category_uuid = detail_category.uuid
            category = Category.create(uuid=category_uuid, name=detail_category.name,
                                       slug=detail_category.slug,
                                       picture=detail_category.picture,
                                       icon=detail_category.icon
                                       )
            categories.append(category)

            for sub_category in detail_category.categories:
                if sub_category.name in result:
                    continue

                sub_category = Category.create(name=sub_category.name,
                                               icon=sub_category.name_url,
                                               subset=category_uuid
                                               )
                categories.append(sub_category)
        with UnitOfWork() as uow:
            uow.session.bulk_save_objects(categories)
            uow.session.commit()
        raise DonFinishedWorkerSpider()

    def _get_categories(self):
        with UnitOfWork() as uow:
            categories_db = uow.session.query(Category.name).all()
            result = [r[0] for r in categories_db]
        return result
