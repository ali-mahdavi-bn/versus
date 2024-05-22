from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, Uuid, DateTime, func

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

attributes_translate_table = Table('attributes_translate', MAPPER_REGISTRY.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('uuid', Uuid, unique=True, nullable=True),
                                   Column('language', Integer, ForeignKey('languages.id')),
                                   Column('attribute_id', Uuid, ForeignKey('attributes.uuid')),
                                   Column('show_name', String(255), nullable=True),
                                   Column('name', String(255), nullable=True),
                                   Column("description", Text, nullable=True),
                                   Column('created_at', DateTime, server_default=func.now()),
                                   Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()),
                                   Column("deleted_at", DateTime)
                                   )
