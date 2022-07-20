"""Formal Language"""
# TODO: Merge this draft work with the existing naive classes.

from _function_coerce import coerce
import log


class FunctionSymbol:
    """

    Bibliography:
        * https://encyclopediaofmath.org/wiki/Signature_(Computer_Science)
    """

    def __init__(self, arity):
        arity = coerce(arity, int)


class ConstantSymbol:
    """A function with arity 0.

    Bibliography:
        * https://encyclopediaofmath.org/wiki/Signature_(Computer_Science)
    """

    def __init__(self):
        super().__init__(arity=0)


class Signature:
    """

    Bibliography:
        * https://encyclopediaofmath.org/wiki/Signature_(Computer_Science)
    """

    def __init__(self, sorts, function_symbols):
        self._sorts = sorts
        self._function_symbols = function_symbols

    @property
    def sorts(self):
        return self._sorts

    @property
    def function_symbols(self):
        return self._function_symbols
