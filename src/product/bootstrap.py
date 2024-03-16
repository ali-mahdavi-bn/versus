from backbone.service_layer.abstract_messagebus import MessageBus
from backbone.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from backbone.service_layer.dependency_injection import inject_dependencies
from backbone.helpers.utils import collect_handlers_functions
from unit_of_work import UnitOfWork
from product.service_layer import command_handlers
from product.service_layer import event_handlers


def bootstrap(
        uow: AbstractUnitOfWork = UnitOfWork(),
) -> MessageBus:
    dependencies = {"uow": uow}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers_functions
        ]
        for event_type, event_handlers_functions in collect_handlers_functions(event_handlers).items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in collect_handlers_functions(command_handlers).items()
    }


    return MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )






