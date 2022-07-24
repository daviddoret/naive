from __future__ import annotations

import jsonpickle
import logging
import warnings
import os
import sys

from naive._exception_naive_warning import NaiveWarning
from naive._exception_naive_error import NaiveError



#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
#logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')


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



