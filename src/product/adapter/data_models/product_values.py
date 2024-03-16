from sqlalchemy import Table, Column, Integer, String, ForeignKey, Uuid, DateTime, func

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

product_value_table = Table('product_values', MAPPER_REGISTRY.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('attribute_id', Uuid, ForeignKey('attributes.uuid')),
                            Column('product_id', Uuid, ForeignKey('products.uuid')),
                            Column('value', String, nullable=True),
                            Column("value_int", Integer, nullable=True),
                            Column('unit', String, nullable=True),
                            Column('created_at', DateTime, server_default=func.now()),
                            Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                            Column("deleted_at", DateTime)
                            )
