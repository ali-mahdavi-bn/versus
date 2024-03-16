from __future__ import annotations

import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING

from .general_types import Command, Event
from unit_of_work import UnitOfWork
if TYPE_CHECKING:
    from unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Command, Event]


class MessageBus:
    def __init__(
            self,
            uow: UnitOfWork,
            event_handlers: Dict[Type[Event], List[Callable]],
            command_handlers: Dict[Type[Command], Callable],
    ):
        self._uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.res = None
        self.queue = []

    @property
    def uow(self):
        return UnitOfWork()

    @property
    def uow_factory(self) -> Callable:
        return UnitOfWork

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")
        return self.res

    def handle_event(self, event: Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self._uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            self.res = handler(command)
            self.queue.extend(self._uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
