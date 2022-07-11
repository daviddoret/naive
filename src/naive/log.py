from __future__ import annotations
import jsonpickle
import logging
import warnings
from _function_coerce import *
from _exception_naive_warning import *
from _exception_naive_error import *


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def stringify_dictionary(**kwargs):
    return jsonpickle.encode(kwargs)


def debug(message: str, **kwargs):
    d = stringify_dictionary(**kwargs)
    message = f'{message}. {d}.'
    logger.debug(message)


def info(message: str, **kwargs):
    d = stringify_dictionary(**kwargs)
    message = f'{message}. {d}.'
    logger.info(message)


def warning(message: str, **kwargs):
    d = stringify_dictionary(**kwargs)
    message = f'{message}. {d}.'
    logger.warning(message, category=NaiveWarning)


def error(message: str, *args, **kwargs):
    d = stringify_dictionary(**kwargs)
    message = f'{message}. {d}.'
    raise NaiveError(message)






