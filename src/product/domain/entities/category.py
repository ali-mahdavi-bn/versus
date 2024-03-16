from datetime import datetime
from uuid import UUID, uuid4

from backbone.adapter.abstract_entity import BaseEntity
from backbone.service_layer.general_types import ID, CreatedAt, UpdatedAt, DeletedAt, IsActive, Slug, Name, \
    ForeignKeyUuid


class Category(BaseEntity):
    id: ID
    uuid: UUID
    name: Name
    slug: Slug
    icon: str
    picture: str
    subset: ForeignKeyUuid
    is_active: IsActive
    created_at: CreatedAt
    updated_at: UpdatedAt
    deleted_at: DeletedAt

    @classmethod
    def create(cls, uuid=None, name=None, subset=None, is_active=True, slug=None, picture=None, icon=None):
        category = Category()
        category.uuid = uuid if uuid else uuid4()
        category.name = name
        category.slug = slug
        category.icon = icon
        category.picture = picture
        category.subset = subset
        category.is_active = is_active

        return category
