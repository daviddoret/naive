# BIBLIOGRAPHY
#   * https://realpython.com/python-modules-packages/


# LOGGING
import logging
logging.info('Naive Package: __setup__.py: starting execution...')
logging.info(f'__name__: {__name__}')

# IMPORTS
from setuptools import setup


# PACKAGE VERSION
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.
logging.info(f'__version__: {__version__}')


setup(name='naive',
      version=__version__,
      description="Under development",
      long_description="",
      author='David Doret',
      author_email='',
      license='MIT',
      packages=['naive'],
      zip_safe=False,
      install_requires=[
            'numpy',
            'nptyping',
            'typing',
            'dataclasses'
          ],
      )

logging.info('Naive Package: __setup__.py: execution completed.')