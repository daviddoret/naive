from abc import ABC
from . import NN1


class VariableIndexPosition(ABC):
    pass


class VariableNN1IndexPosition(int, NN1):
    pass


class VariableIndexes(ABC):
    """The variable indexes is a list of 0 or more indexes that, with the base name, compose the variable indexed name.

    """

class VariableNN1Indexes(VariableIndexes):
    """Provides support for the common situation where indexes"""
