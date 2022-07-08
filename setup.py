from setuptools import setup
import importlib.metadata
# PACKAGE VERSION
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.

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
