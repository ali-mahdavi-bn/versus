from sqlalchemy import Table, Column, Integer, String, DateTime

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

user_table = Table('users', MAPPER_REGISTRY.metadata,
                   Column('id', Integer, primary_key=True),
                   Column("name", String(255), nullable=True),
                   Column("email", String(100), nullable=True),
                   Column("deleted_at", DateTime)
                   )
