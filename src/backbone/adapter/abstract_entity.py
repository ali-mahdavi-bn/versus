import copy
import datetime
from dataclasses import dataclass
from uuid import UUID



class BaseEntity:
    def normalize_dict(self):
        d = {}
        for attr, value in self.__dict__.items():
            if attr in ("events", "_sa_instance_state"):
                continue
            value = value.__str__() if isinstance(value, UUID) else value
            value = value.isoformat() if isinstance(value, datetime.time) or isinstance(value, datetime.date) else value
            value = value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime.datetime) else value
            d[attr] = value
        return d

    def __str__(self):
        _str = ""
        if hasattr(self, "uuid"):
            _str += f"{self.uuid}|"
        if hasattr(self, "id"):
            _str += f"{self.id}|"
        if hasattr(self, "title"):
            _str += f"{self.title}|"
        if hasattr(self, "name"):
            _str += f"{self.name}|"
        return _str

    def __repr__(self):
        _str = ""
        if hasattr(self, "uuid"):
            _str += f"{self.uuid}|"
        if hasattr(self, "id"):
            _str += f"{self.id}|"
        if hasattr(self, "title"):
            _str += f"{self.title}|"
        if hasattr(self, "name"):
            _str += f"{self.name}|"
        return _str

    @classmethod
    def factory(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            if hasattr(instance, key):
                if isinstance(getattr(instance, key), BaseEntity) or isinstance(getattr(instance, key), list):
                    pass
                    # setattr(instance, key, getattr(instance, key).factory(**value))
                else:
                    setattr(instance, key, value)
        return instance


@dataclass
class BaseDTO:
    pass
