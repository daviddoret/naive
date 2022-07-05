from __future__ import annotations
import abc
import src.naive.settings as settings
import src.naive.variable as variable
import src.naive.coerce as coerce


class VariableContent(abc.ABC):
    """An abstract class for anything that may be used as variable value content, e.g. a constant, an unknown value, or a formula."""
    pass


class Constant(VariableContent):
    """An abstract class for constant value contents."""
    pass


class Unknown(VariableContent):
    """A special value for unknown values.

    Todo:
        * Consider implementing this as a singleton."""

    def __str__(self):
        return settings.UNKNOWN_NOTATION


"""The 'unknown value' special constant."""
unknown = Unknown()
