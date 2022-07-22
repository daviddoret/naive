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

COERCION_SUCCESS = 1
COERCION_FAILURE = 2

code_exclusion_list = [1]

def stringify_dictionary(**kwargs):
    s = ''
    for k, v in kwargs.items():
        s = f'{s}\n  {k}: {str(v)}'
    return s
    # return jsonpickle.encode(kwargs)


def debug(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{code}: {message} {d}.'
        logger.debug(message)


def info(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{message} {d}.'
        logger.info(message)


def warning(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{code}: {message}. {d}.'
        logger.warning(message)


def error(message: str = '', *args, code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{code}: {message}. {d}.'
        logging.error(message, exc_info=True)
        # raise NaiveError(message)





