from sqlalchemy import Table, Column, Integer, String, ForeignKey

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

enumeration_table = Table('enumerations', MAPPER_REGISTRY.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('title', String(100)),
                          Column('parent_id', Integer, ForeignKey('enumerations.id'))
                          )
