
from backbone.configs import Config
from backbone.container.injector import DependencyContainer, CallableDependency, SingletonDependency
from backbone.helpers.colors import Color
from backbone.helpers.translator import Translator
from backbone.infrastructure.log._logger import Logger
from unit_of_work import UnitOfWork


class Container(DependencyContainer):
    color = SingletonDependency(Color)
    config = SingletonDependency(Config)
    # minio = SingletonDependency(MinioBucketManager)
    translator = SingletonDependency(Translator)
    uow = CallableDependency(UnitOfWork)
    logger = SingletonDependency(Logger)


class Provider:

    def __class_getitem__(cls, key):
        containers = DependencyContainer.__subclasses__()
        for container in containers:
            members = container.get_members()
            for member in members:
                if member == key:
                    if hasattr(member, "initialize_dependency"):
                        return member.initialize_dependency()
                    return member
