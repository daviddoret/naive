import abc
import src.naive.settings as settings


class VariableValue(abc.ABC):
    """An abstract class for mathematical variable values."""
    pass


class UnknownValue(VariableValue):
    """A special value for unknown values."""
    def __str__(self):
        return settings.VARIABLE_UNKNOWN_VALUE


"""The 'unknown value' constant."""
variable_unknown_value = UnknownValue()
