from abc import ABC, abstractmethod


class AbstractCommand(ABC):

    @abstractmethod
    def run_command(self): pass


class BaseCommand(AbstractCommand):
    def run_command(self):
        pass
