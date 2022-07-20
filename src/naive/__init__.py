from __future__ import annotations
import logging
logging.info('Naive Package Initialization: Starting')
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.
logging.info(f'__version__: {__version__}')

import core
import ba1

# LOGGING
logging.info('Naive Package Initialization: Completed')
