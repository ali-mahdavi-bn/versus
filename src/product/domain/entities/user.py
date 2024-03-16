from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, Name


class User(BaseEntity):
    id: ID
    name: Name
    email: str
