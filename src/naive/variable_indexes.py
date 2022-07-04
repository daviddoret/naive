from abc import ABC
from src.naive.natural_number_1_value import NaturalNumber1Value, NN1V
import src.naive.settings as settings


class VariableIndexPosition(ABC):
    pass


class VariableNN1IndexPosition(NN1V, int):
    def __new__(cls, *args, **kwargs):
        super().__new__(cls, *args, **kwargs)


class VariableIndexes(ABC):
    """The variable indexes is a list of 0 or more indexes that, with the base name, compose the variable indexed name.
    """
    pass


class VariableNoIndex(VariableIndexes):
    """When a variable has no index (e.g. 'x'), it is assigned the NoIndex index."""
    def __str__(self):
        return settings.VARIABLE_NO_INDEX


"""The 'no index' constant for variables with non index."""
variable_no_index = VariableNoIndex()


class VariableNN1Indexes(VariableIndexes):
    """Provides support for the common situation where indexes"""
    pass