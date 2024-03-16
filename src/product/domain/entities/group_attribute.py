from datetime import datetime
from uuid import UUID, uuid4

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, Name, CreatedAt, UpdatedAt, DeletedAt


class GroupAttribute(BaseEntity):
    id: ID
    uuid: UUID
    name: Name
    icon: str
    label: str
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, name=None, icon=None, label=None, uuid=None):
        group_attribute = GroupAttribute()
        group_attribute.uuid = uuid if uuid else uuid4()
        group_attribute.name = name
        group_attribute.icon = icon
        group_attribute.label = label

        return group_attribute
