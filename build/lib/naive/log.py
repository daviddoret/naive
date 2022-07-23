from __future__ import annotations
import jsonpickle
import logging
import warnings
from _function_coerce import *
from _exception_naive_warning import *
from _exception_naive_error import *

import os
import sys

#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
#logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')

# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
# Reference: https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
logging.basicConfig(format='%(message)s')

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
# Reference: https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
logging.root.setLevel(logging.INFO)

def set_debug_level():
    logging.root.setLevel(logging.DEBUG)

def set_info_level():
    logging.root.setLevel(logging.INFO)

def set_warning_level():
    logging.root.setLevel(logging.WARNING)

def set_error_level():
    logging.root.setLevel(logging.ERROR)

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
# Reference: https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
#logging.basicConfig(level=logging.NOTSET)

# Create a custom logger
logger = logging.getLogger('naive')

# Create handlers
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_format = logging.Formatter('%(message)s')
stdout_handler.setFormatter(stdout_format)
#logger.addHandler(stdout_handler)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stderr_handler.setFormatter(stderr_format)
#logger.addHandler(stderr_handler)

logfile_handler = logging.FileHandler('naive.log')
logfile_handler.setLevel(logging.WARNING)
logfile_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logfile_handler.setFormatter(logfile_format)
#logger.addHandler(logfile_handler)


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
    global logger
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'DEBUGGING: {message} {d}.'
        logger.debug(message)


def info(message: str = '', code: int = 0, **kwargs):
    global logger
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{message} {d}'
        logging.info(message)


def warning(message: str = '', code: int = 0, **kwargs):
    global logger
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'WARNING: {message} {d}'
        logger.warning(message)


def error(message: str = '', *args, code: int = 0, **kwargs):
    global logger
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'ERROR: {message}. {d}.'
        logger.error(message, exc_info=True)
        raise NaiveError(message)





