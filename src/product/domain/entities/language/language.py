from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, Name


class Language(BaseEntity):
    id: ID
    name: Name
