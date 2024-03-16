from typing import Any, Dict, List

from backbone.adapter.abstract_entity import BaseEntity
from backbone.api.abstract_api_resource import AbstractApiResource
from backbone.api.translator.translatore import translate


class BaseCommandResource(AbstractApiResource):
    def make(self, model: Any, message="", lang="fa") -> Dict:
        data = None
        if isinstance(model, dict):
            data = model
            message = translate(parser=message, entity="", dictionary_type="phrases", lang=lang)
        elif isinstance(model, BaseEntity):
            if hasattr(model, "uuid"):
                _uuid = model.uuid
                data = {"uuid": _uuid}
            elif hasattr(model, "id"):
                _uuid = model.id
                data = {"id": _uuid}
            entity = translate(type(model).__name__, dictionary_type="entity", lang=lang)
            message = translate(message, entity=entity, dictionary_type="phrases", lang=lang)
        else:
            data = model
            message = translate(message, entity="", dictionary_type="phrases", lang=lang)
        return self.json(
            message=message,
            data={"data": data},
        )


class PaginationApiResource:
    @classmethod
    def make(cls, models: List[Dict], count: int) -> Dict:
        return cls.json(
            count=count,
            data=models,
        )

    @classmethod
    def json(cls, **kwargs) -> Dict:
        return {**kwargs}
