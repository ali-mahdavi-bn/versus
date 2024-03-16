from sqlalchemy.orm import declared_attr, declarative_base
from sqlalchemy.orm import registry


class CustomBase:

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    pass


BaseModel = declarative_base(cls=CustomBase)
MAPPER_REGISTRY = registry()
