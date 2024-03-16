import contextlib
from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Optional, Callable, Any, Dict

T = TypeVar('T')


class DependencyContainer:
    @classmethod
    def get_members(cls):
        return [item[1] for item in cls.__dict__.items() if not item[0].startswith("__")]


class AbstractDependencyInitializer(ABC):

    @abstractmethod
    def initialize_dependency(self): raise NotImplementedError


class SingletonDependency(AbstractDependencyInitializer):
    __instance: Optional[T] = None
    __instance_n: Optional[T] = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance = super().__new__(cls)
    #     return cls.__instance

    def __init__(self, ref: Callable[..., T], **kwargs: Any) -> None:
        if not self.__instance_n:
            self.__instance_n = ref(**kwargs)


    def initialize_dependency(self) -> T:
        return self.__instance_n


class CallableDependency(AbstractDependencyInitializer):
    __callable: Optional[Callable[..., T]] = None

    def __init__(self, ref, **kwargs):
        self.__callable = ref
        self.arguments: Dict[str, Any] = kwargs

    def initialize_dependency(self) -> T:
        return self.__callable(**self.arguments)


class RetryableCallableDependency(AbstractDependencyInitializer):
    __callable: Optional[Callable[..., T]] = None

    def __init__(self, ref: Callable[..., T], retry_count: int = 1, **kwargs: Any) -> None:
        self.__callable = ref
        self.__retry_count = retry_count
        self.arguments: Dict[str, Any] = kwargs

    def initialize_dependency(self) -> T:
        for _ in range(self.__retry_count):
            with contextlib.suppress(Exception):
                return self.__callable(**self.arguments)
