import json
from typing import List

from backbone.crawler.helper.helpers.requests import RequestArgs
from backbone.crawler.helper.helpers.response import Response
from backbone.crawler.spider import Spider
from product.domain.entities import Category, ProductUrl
from unit_of_work import UnitOfWork


class ProductVersusSpider(Spider):
    name = "versus_spider"

    def __init__(self):
        self.subset_category = None

    def start_requests(self, **kwargs):

        with UnitOfWork() as uow:
            categories_db = uow.session.query(Category.id, Category.icon, Category.subset).all()
            for id, icon, subset in categories_db:
                if not subset:
                    continue

                self.subset_category = subset
                self._end_url = icon
                url = f"https://versus.com/en/{self._end_url}"
                yield RequestArgs(url=url, callback=self.parse)

    def parse(self, response: Response):
        url_product = self._get_url_product()
        self.products: List[ProductUrl] = []
        page_number: int = 1
        obj_tags = response.find_all(tag="a", class_="Item__link___3uW-Z")
        if obj_tags:
            for obj_tag in obj_tags:
                url_product_client = obj_tag.get("href")
                if url_product_client not in url_product:
                    product = ProductUrl.create(url=url_product_client, category_id=self.subset_category)
                    self.products.append(product)
            for i in range(page_number):
                yield RequestArgs(url=f"https://versus.com/api/top/en/{self._end_url}?page={str(i)}",
                                  callback=self.parse_more)
            self.save_product()

    def parse_more(self, response: Response):
        products = json.loads(response.content.decode("utf-8"))
        for product in products.get("toplist"):
            url = f"/en/{str(product.get('name_url'))}"

            product = ProductUrl.create(url=url, category_id=self.subset_category)
            self.products.append(product)

    def save_product(self):
        with UnitOfWork() as uow:
            uow.session.bulk_save_objects(self.products)
            uow.session.commit()

    def _get_url_product(self):
        with UnitOfWork() as uow:
            product_db = uow.session.query(ProductUrl.url).all()
            result = [r[0] for r in product_db]
        return result
