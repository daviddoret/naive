from __future__ import annotations
import naive.log
#import log
naive.log.info('Naive initialization started.')
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '0.0.3'  # Initial version for the first build.
naive.log.info(f'Naive version: {__version__}')

import naive.core
import naive.ba1
import naive.rformats
import naive.glyphs
import naive.parsing

# LOGGING
naive.log.info('Naive initialization completed.')
