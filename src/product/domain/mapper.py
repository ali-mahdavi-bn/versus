from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from product.adapter import data_models
from product.domain import entities


def start_mapper():
    # Category
    MAPPER_REGISTRY.map_imperatively(entities.Category, data_models.category_table)
    # Attribute
    MAPPER_REGISTRY.map_imperatively(entities.Attributes, data_models.attribute_table)
    MAPPER_REGISTRY.map_imperatively(entities.AttributeTranslate, data_models.attributes_translate_table)
    MAPPER_REGISTRY.map_imperatively(entities.GroupAttribute, data_models.group_attribute_table)
    # Language
    MAPPER_REGISTRY.map_imperatively(entities.Language, data_models.language_table)
    # Product
    MAPPER_REGISTRY.map_imperatively(entities.Product, data_models.product_table)
    MAPPER_REGISTRY.map_imperatively(entities.ProductTranslate, data_models.product_translate_table)
    MAPPER_REGISTRY.map_imperatively(entities.ProductValue, data_models.product_value_table)
    MAPPER_REGISTRY.map_imperatively(entities.ProductUrl, data_models.product_url_table)
    # User
    MAPPER_REGISTRY.map_imperatively(entities.User, data_models.user_table)
