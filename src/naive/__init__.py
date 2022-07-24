from __future__ import annotations

import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '0.0.3'  # Initial version for the first build.

from core import *

logging.info(f'Naive initialization completed. Package version: {__version__}.')
