import logging
import re

import datetime
import pytz
from structlog import get_logger
from structlog.processors import _json_fallback_handler
from backbone.infrastructure.log import json


# from sentry.utils import json, metrics


def now() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone("Asia/Tehran"))


_default_encoder = json.JSONEncoder(
    separators=(",", ":"),
    ignore_nan=True,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    encoding="utf-8",
    default=_json_fallback_handler,
).encode

# These are values that come default from logging.LogRecord.
# They are defined here:
# https://github.com/python/cpython/blob/2.7/Lib/logging/__init__.py#L237-L310
throwaways = frozenset(
    (
        "threadName",
        "thread",
        "created",
        "process",
        "processName",
        "args",
        "module",
        "filename",
        "levelno",
        "exc_text",
        "msg",
        "pathname",
        "lineno",
        "funcName",
        "relativeCreated",
        "levelname",
        "msecs",
    )
)


class JSONRenderer:
    def __call__(self, logger, name, event_dict):
        return _default_encoder(event_dict)


class HumanRenderer:
    def __call__(self, logger, name, event_dict):
        level = event_dict.pop("level")
        real_level = level.upper() if isinstance(level, str) else logging.getLevelName(level)
        base = "{} [{}] {}: {}".format(
            now().strftime("%H:%M:%S"),
            real_level,
            event_dict.pop("name", "root"),
            event_dict.pop("event", ""),
        )
        join = " ".join(k + "=" + repr(v) for k, v in event_dict.items())
        return "{}{}".format(base, (" (%s)" % join if join else ""))


class StructLogHandler(logging.StreamHandler):
    def get_log_kwargs(self, record, logger):
        kwargs = {k: v for k, v in vars(record).items() if k not in throwaways and v is not None}
        kwargs.update({"level": record.levelno, "event": record.msg})

        if record.args:
            # record.args inside of LogRecord.__init__ gets unrolled
            # if it's the shape `({},)`, a single item dictionary.
            # so we need to check for this, and re-wrap it because
            # down the line of structlog, it's expected to be this
            # original shape.
            if isinstance(record.args, (tuple, list)):
                kwargs["positional_args"] = record.args
            else:
                kwargs["positional_args"] = (record.args,)

        return kwargs

    def emit(self, record, logger=None):
        # If anyone wants to use the 'extra' kwarg to provide context within
        # structlog, we have to strip all of the default attributes from
        # a record because the RootLogger will take the 'extra' dictionary
        # and just turn them into attributes.
        if logger is None:
            logger = get_logger()
        logger.log(**self.get_log_kwargs(record=record, logger=logger))


class MessageContainsFilter(logging.Filter):
    """
    A logging filter that allows log records where the message
    contains given substring(s).

    contains -- a string or list of strings to match
    """

    def __init__(self, contains):
        if not isinstance(contains, list):
            contains = [contains]
        if not all(isinstance(c, str) for c in contains):
            raise TypeError("'contains' must be a string or list of strings")
        self.contains = contains

    def filter(self, record):
        message = record.getMessage()
        return any(c in message for c in self.contains)


whitespace_re = re.compile(r"\s+")
metrics_badchars_re = re.compile("[^a-z0-9_.]")
