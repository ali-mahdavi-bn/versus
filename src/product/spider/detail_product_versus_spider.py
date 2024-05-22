import json
from typing import List
from uuid import uuid4, UUID

from backbone.crawler.helper.helpers.requests import RequestArgs
from backbone.crawler.helper.helpers.response import Response
from backbone.crawler.spider import Spider
from product.domain.entities import Product, ProductUrl, Attributes, AttributeTranslate, ProductValue, \
    ProductTranslate, GroupAttribute, Category
from unit_of_work import UnitOfWork


class DetailProductVersusSpider(Spider):
    name = "versus_spider"
    translate_categories = []
    category_attribute = []
    products_translate = []
    products = []
    product_values = []
    product_value_attributes = []
    group_attributes = []
    new_categories_name: dict = {}
    new_group_attribute: dict = {}

    def __init__(self):
        self.uuid_group_attribute = None

    def start_requests(self, **kwargs):
        with UnitOfWork() as uow:
            product_url = uow.session.query(ProductUrl.id, ProductUrl.url, ProductUrl.category_id).all()

            for id, url, category_id in product_url:
                self.category_id = category_id
                url = (
                        f"https://versus.com/api/store/f5p{url}"
                        + f"?ts={self.unix_time_now()}&userId=&type=json"
                )
                yield RequestArgs(url=url, callback=self.parse_detail)
                # yield RequestArgs(url=url, callback=self.parse_detail_a)
            self.delete_product_url_with_id(id=id)

    def delete_product_url_with_id(self, id):
        with UnitOfWork() as uow:
            product_url = uow.product_url.find_by_id(id)
            uow.session.delete(product_url)

    def parse_detail_a(self, response: Response):
        categories_name = self.get_all_name_category()
        group_attributes = self.get_all_group_attributes()
        products = json.loads(response.content.decode("utf-8"))
        category_attributes = products.get("comparison").get("tldr")
        category_attributes_and_groups = products.get("comparison").get("propGroups")
        name_current_product = products.get("objects").get(next(iter(products.get("objects")))).get("name")
        translate_attribute_language = 2
        for category_attribute in category_attributes:
            for i in category_attribute:
                name_category = i.get("name")
                translate_attribute_uuid: UUID = uuid4()
                attribute_uuid: UUID = uuid4()
                translate_attribute_show_name = i.get("ax")
                translate_attribute_description = i.get("x")
                unit_attribute = i.get('unit')

                self.add_translate_category(uuid=translate_attribute_uuid, name=name_category,
                                            show_name=translate_attribute_show_name,
                                            category_attribute_id=attribute_uuid,
                                            description=translate_attribute_description,
                                            language=translate_attribute_language)

                self.add_attribute(uuid=attribute_uuid, translate_category_id=2,
                                   category_attribute_type=unit_attribute,
                                   category_id=self.category_id)

    def a_attribute(self):
        ...

    def parse_detail(self, response: Response):
        categories_name = self.get_all_name_category()
        group_attributes = self.get_all_group_attributes()
        products = json.loads(response.content.decode("utf-8"))
        category_attributes = products.get("comparison").get("tldr")
        category_attributes_and_groups = products.get("comparison").get("propGroups")
        name_current_product = products.get("objects").get(next(iter(products.get("objects")))).get("name")

        for category_attribute in category_attributes:
            product_uuid = uuid4()
            for i in category_attribute:
                category_attribute_uuid = uuid4()
                name_category = i.get("name")
                self.generate_product_category(name_category=name_category, categories_name=categories_name,
                                               show_name=i.get("ax"),
                                               description_translate_category=i.get("x"),
                                               translate_category_language=2, unit_product_value=i.get("unit"),
                                               product_uuid=product_uuid, product_value=i.get("v"),
                                               category_attribute_uuid_=category_attribute_uuid)

            for category_attributes_and_group in category_attributes_and_groups:
                group_name = category_attributes_and_group.get("name")

                self.add_group_attribute(name=group_name,
                                         group_attributes=group_attributes,
                                         icon=category_attributes_and_group.get("icon"),
                                         label=category_attributes_and_group.get("label"))

                for reason in category_attributes_and_group.get("reasons"):
                    category_attribute_uuid: UUID = uuid4()
                    name_category: str = reason.get("name")
                    self.generate_product_category(name_category=name_category, categories_name=categories_name,
                                                   show_name=reason.get("ax"),
                                                   smaller_better=reason.get("smaller_better"),
                                                   description_translate_category=reason.get("x"),
                                                   translate_category_language=2,
                                                   unit_product_value=reason.get("unit"),
                                                   product_uuid=product_uuid, product_value=reason.get("votes"),
                                                   category_attribute_type=reason.get("kind"),
                                                   category_attribute_uuid_=category_attribute_uuid)

            self.add_product_and_translate(product_uuid=product_uuid,
                                           category_id=self.category_id, product_name=name_current_product, language=2)

        self.save_all_object()

    def generate_product_category(self, name_category: str, categories_name: list, show_name: str,
                                  description_translate_category: str,
                                  translate_category_language: int, unit_product_value: str,
                                  product_uuid,
                                  product_value, category_attribute_uuid_, category_attribute_type: str = None,
                                  smaller_better=None):
        conditional_create_category_attribute: bool = name_category in categories_name
        conditional_create_category_attribute_new: bool = self.new_categories_name.get(name_category)
        category_attribute_uuid: UUID = category_attribute_uuid_ if not conditional_create_category_attribute and not conditional_create_category_attribute_new else conditional_create_category_attribute_new
        if not conditional_create_category_attribute and not conditional_create_category_attribute_new:
            translate_category_uuid: UUID = uuid4()
            self.add_translate_category(uuid=translate_category_uuid, name=name_category,
                                        show_name=show_name,
                                        category_attribute_id=category_attribute_uuid,
                                        description=description_translate_category,
                                        language=translate_category_language)
            self.add_attribute(uuid=category_attribute_uuid,
                               slug=name_category,
                               smaller_better=smaller_better,
                               category_attribute_type=category_attribute_type,
                               translate_category_id=translate_category_uuid,
                               category_id=self.category_id)
            self.new_categories_name[name_category] = category_attribute_uuid

        self.add_product_value(unit=unit_product_value, product_uuid=product_uuid, value=product_value,
                               category_attribute_uuid=category_attribute_uuid)

    def add_group_attribute(self, name=None, group_attributes=None, icon=None, label=None):
        new_group_attribute = self.new_group_attribute.get(name)
        if name not in group_attributes and not new_group_attribute:
            self.uuid_group_attribute: UUID = uuid4()
            group_attribute: GroupAttribute = GroupAttribute.create(uuid=self.uuid_group_attribute, name=name,
                                                                    icon=icon,
                                                                    label=label)
            self.group_attributes.append(group_attribute)
            self.new_group_attribute[name] = self.uuid_group_attribute

        elif new_group_attribute:
            self.uuid_group_attribute = new_group_attribute
        else:
            self.uuid_group_attribute = self.get_group_attribute_with_name(name)

    def add_translate_category(self, uuid, name, show_name, description, language, category_attribute_id=None):
        translate_category: AttributeTranslate = AttributeTranslate.create(uuid=uuid,
                                                                           name=name.lower().strip() if name else None,
                                                                           show_name=show_name.lower().strip() if show_name else name.replace(
                                                                               "_", ' ').replace("_", " ").title(),
                                                                           description=description.lower().strip(),
                                                                           category_attribute_id=category_attribute_id,
                                                                           language=language)
        self.translate_categories.append(translate_category)

    def get_all_name_category(self):
        with UnitOfWork() as uow:
            categories = uow.session.query(Category.name).all()
            return [i[0] for i in categories]

    def get_all_group_attributes(self):
        with UnitOfWork() as uow:
            categories_attributes = uow.session.query(GroupAttribute.name).all()
            return [i[0] for i in categories_attributes]

    def get_group_attribute_with_name(self, name):
        with UnitOfWork() as uow:
            categories_attributes = uow.session.query(GroupAttribute.uuid).filter(GroupAttribute.name == name).first()
            return categories_attributes[0]

    def add_attribute(self, uuid,
                      translate_category_id,
                      slug,
                      category_attribute_type,
                      category_id,
                      smaller_better=None):
        category_attribute_obj: Attributes = Attributes.create(uuid=uuid,
                                                               type=category_attribute_type,
                                                               slug=slug,
                                                               group_attribute_id=self.uuid_group_attribute,
                                                               translate_category_id=translate_category_id,
                                                               smaller_better=smaller_better,
                                                               category_id=category_id)

        self.category_attribute.append(category_attribute_obj)

    def add_product_and_translate(self, product_uuid,
                                  category_id, product_name, language=2):
        translate_product_uuid: UUID = uuid4()
        product_translate: ProductTranslate = ProductTranslate.create(uuid=translate_product_uuid,
                                                                      name=product_name.lower().strip() if product_name else "",
                                                                      language=language, product_id=product_uuid)
        product: Product = Product.create(uuid=product_uuid, slug=product_name.lower().strip().replace(
            "_", ' ').replace("_", " ") if product_name else "", category_id=category_id)
        self.products.append(product)
        self.products_translate.append(product_translate)

    def add_product_value(self, unit, product_uuid, value, category_attribute_uuid):
        if isinstance(value, int):
            product_value: ProductValue = ProductValue.create(unit=unit, value_int=value, product_id=product_uuid,
                                                              category_attribute_id=category_attribute_uuid)
        elif isinstance(value, str) and value.isdigit():
            product_value: ProductValue = ProductValue.create(unit=unit, value_int=int(value), product_id=product_uuid,
                                                              category_attribute_id=category_attribute_uuid)
        else:
            product_value: ProductValue = ProductValue.create(unit=unit, value=value, product_id=product_uuid,
                                                              category_attribute_id=category_attribute_uuid)

        self.product_values.append(product_value)

    def save_all_object(self):
        self.products.extend(self.products_translate)
        self.products.extend(self.group_attributes)
        self.products.extend(self.category_attribute)
        self.products.extend(self.translate_categories)
        self.products.extend(self.product_values)
        with UnitOfWork() as uow:
            uow.session.bulk_save_objects(self.products)
            uow.session.commit()

        self.none_list()

    def none_list(self):
        self.products_translate: List[ProductTranslate] = []
        self.products: List[Product] = []
        self.translate_categories: List[AttributeTranslate] = []
        self.category_attribute: List[Attributes] = []
        self.product_values: List[ProductValue] = []
        self.group_attributes: List[GroupAttribute] = []

    def unix_time_now(self):
        import datetime
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000
        return int(unix_timestamp)
