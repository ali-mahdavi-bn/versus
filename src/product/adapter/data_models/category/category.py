from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, Uuid, DateTime, func

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

category_table = Table('categories', MAPPER_REGISTRY.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('uuid', Uuid, unique=True),
                       Column('name', String(255), unique=True),
                       Column('slug', String(255), unique=True),
                       Column('icon', String(255)),
                       Column('picture', String(255)),
                       Column('subset', Uuid, ForeignKey('categories.uuid'), nullable=True),
                       Column("is_active", Boolean, default=True),
                       Column('created_at', DateTime, server_default=func.now()),
                       Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                       Column("deleted_at", DateTime)

                       )
