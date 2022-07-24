# BIBLIOGRAPHY
#   * https://realpython.com/python-modules-packages/


# LOGGING
import logging
logging.info('Naive package setup: STARTED.')
#logging.info(f'__name__: {__name__}')

# IMPORTS
from setuptools import setup


# PACKAGE VERSION
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '0.0.3'
logging.info(f'Version: {__version__}')


setup(name='naive',
      version=__version__,
      description="Under development",
      long_description="",
      author='David Doret',
      author_email='',
      license='MIT',
      packages=['naive'],
      package_dir={'naive': 'src/naive'},
      package_data={'naive': ['data/*.*']},
      zip_safe=False,
      install_requires=[
            'typing',
            'dataclasses',
            'textx'
          ],
      )

logging.info('Naive package setup: COMPLETED.')
