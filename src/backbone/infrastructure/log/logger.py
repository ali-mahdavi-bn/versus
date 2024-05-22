import sys
from abc import ABC, abstractmethod

from loguru import logger as loguru_logger

from backbone.configs import config


class ILogger(ABC):
    @abstractmethod
    def debug(self, message, **kwargs):
        pass

    @abstractmethod
    def info(self, message, **kwargs):
        pass

    @abstractmethod
    def error(self, message, **kwargs):
        pass

    @abstractmethod
    def exception(self, message, **kwargs):
        pass

    @abstractmethod
    def warning(self, message, **kwargs):
        pass


class Logger():

    def __init__(self):
        self.loguru_logger = loguru_logger

    def debug(self, message, **kwargs):
        self.loguru_logger.debug(message, **kwargs)

    @abstractmethod
    def info(self, message, **kwargs):
        self.loguru_logger.info(message, **kwargs)

    @abstractmethod
    def error(self, message, **kwargs):
        self.loguru_logger.error(message, **kwargs)

    @abstractmethod
    def exception(self, message, **kwargs):
        self.loguru_logger.exception(message, **kwargs)

    @abstractmethod
    def warning(self, message: object, **kwargs: object) -> object:
        self.loguru_logger.warning(message, **kwargs)


#
#
# class LoggerFactory:
#     def __init__(self):
#         structlog.configure(
#             processors=[
#                 structlog.stdlib.add_log_level,
#                 structlog.stdlib.PositionalArgumentsFormatter(),
#                 structlog.processors.StackInfoRenderer(),
#                 structlog.processors.format_exc_info,
#                 structlog.processors.UnicodeDecoder(),
#                 structlog.processors.JSONRenderer(),
#             ],
#             logger_factory=structlog.PrintLoggerFactory(),
#         )
#
#         self.loguru_logger = loguru_logger
#
#     def getLogger(self, name):
#         logger = structlog.wrap_logger(self.loguru_logger)
#         logger = logger.bind(logger_name=name)
#         return logger


def logger_name(name: any) -> str:
    if type(name) == str:
        return name

    if type(name) == type:
        return f"{name.__module__}.{name.__name__}"

    if hasattr(name, '__class__'):
        return f"{name.__class__.__module__}.{name.__class__.__name__}"

    try:
        return f"{name.__module__}.{name.__name__}"
    except:
        return str(name)


class LoggerFactory:
    _loggers = {}

    @classmethod
    def get_logger(cls, _name):
        if _name not in cls._loggers:
            # logger = LLogger(
            #     core=_Core(),
            #     exception=None,
            #     depth=0,
            #     record=False,
            #     lazy=False,
            #     colors=False,
            #     raw=False,
            #     capture=True,
            #     patchers=[],
            #     extra={},
            # )
            loguru_logger.remove()

            if not config.DEBUG:
                loguru_logger.add(sys.stdout, format="", serialize=True, level="TRACE")
            else:
                loguru_logger.add(
                    sys.stdout,
                    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> -> <level>{message}</level>",
                    level="TRACE",
                )
            logger = loguru_logger.bind(class_name=logger_name(_name))
            cls._loggers[_name] = logger

        return cls._loggers[_name]



