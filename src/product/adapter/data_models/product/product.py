from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, Uuid, String, DateTime, func

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

product_table = Table('products', MAPPER_REGISTRY.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('uuid', Uuid, unique=True, nullable=True),
                      Column("image_src", String, nullable=True),
                      Column("slug", String, nullable=True),
                      Column('category_id', Uuid, ForeignKey('categories.uuid')),
                      Column("is_active", Boolean, default=True),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                      Column("deleted_at", DateTime)
                      )
