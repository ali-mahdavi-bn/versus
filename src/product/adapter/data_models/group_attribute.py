from sqlalchemy import Table, Column, Integer, String, Uuid, DateTime, func

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

group_attribute_table = Table('group_attributes', MAPPER_REGISTRY.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('uuid', Uuid, unique=True),
                              Column('name', String(255)),
                              Column('icon', String),
                              Column('label', String),
                              Column('created_at', DateTime, server_default=func.now()),
                              Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                              Column("deleted_at", DateTime)
                              )
