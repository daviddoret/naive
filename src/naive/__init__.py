from __future__ import annotations
import logging
#import log
#log.info('Naive initialization started.')
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '0.0.2'  # Initial version for the first build.
#log.info(f'Naive version: {__version__}')

import core
import ba1
import rformats
import glyphs
import parsing

# LOGGING
#log.info('Naive initialization completed.')
