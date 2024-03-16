from sqlalchemy import Table, Column, Integer, Uuid, String, ForeignKey

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

product_url_table = Table('products_url', MAPPER_REGISTRY.metadata,
                          Column('id', Integer, primary_key=True),
                          Column("url", String, nullable=True),
                          Column("category_id", Uuid, ForeignKey("categories.uuid"), nullable=True),
                          )
