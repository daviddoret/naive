from setuptools import setup
import importlib.metadata
__version__ = importlib.metadata.version('naive')

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
