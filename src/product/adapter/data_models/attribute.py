from sqlalchemy import Table, Column, Integer, ForeignKey, Uuid, DateTime, func, String, Boolean

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

attribute_table = Table('attributes', MAPPER_REGISTRY.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('uuid', Uuid, unique=True, nullable=True),
                        Column('category_id', Uuid, ForeignKey('categories.uuid'), nullable=True),
                        Column('group_attribute_id', Uuid, ForeignKey('group_attributes.uuid'),
                               nullable=True),
                        Column('slug', String(255), unique=True),
                        Column('is_searchable', Boolean, default=False),
                        Column('is_show', Boolean, default=False),
                        Column('smaller_better', Boolean, default=False),
                        Column('created_at', DateTime, server_default=func.now()),
                        Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                        Column("deleted_at", DateTime)
                        )
