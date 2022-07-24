from __future__ import annotations
import logging
import log
log.info('Naive initialization started.')
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.
log.info(f'Naive version: {__version__}')

import core
import ba1_module
import rformats
import glyphs

# LOGGING
log.info('Naive initialization completed.')
