from abc import ABC, abstractmethod

from backbone.exception.logical_validation_exeption.exeptions import LogicalValidationException


class AbstractValidator(ABC):

    def __init__(self, loc: str) -> None:
        self._loc = loc

    @abstractmethod
    def type(self) -> str:
        pass

    def message(self) -> str:
        return f"validation.{self.type()}"

    @abstractmethod
    def passes(self) -> bool:
        pass

    def validate(self) -> None:
        if not self.passes():
            raise LogicalValidationException(message=self.message(), location=self._loc, type_=self.type())
