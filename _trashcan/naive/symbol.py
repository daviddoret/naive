from __future__ import annotations
import typing
import warnings
from .coercion_error import CoercionError
from .coercion_warning import CoercionWarning
from .scope_management import Scope
from .scope_management import ImplicitContext


class Symbol:
    """A mathematical symbol.

    Mainly used as an abstract class to derive mathematical symbols.

    """
    def __init__(s: ImplicitSymbol = None, c: ImplicitContext = None):
        """Instantiates a new **Symbol**.

        If **s** is None: generate a symbol name automatically.

        If **c** is None: add the symbol to the default user context.

        Args:
            s (ImplicitSymbol): A symbol name.

        Returns:
            Symbol: A new natural number.

        Raises:
            CoercionWarning: If ambiguous type coercion was necessary.
            CoercionError: If type coercion failed.

        Example:

            .. jupyter-execute::

                import naive
                s = naive.Symbol('x')
                print(type(s))
                print(s)

        """

        if o is None:
            o = 0
            warnings.warn(f'None coerced to 0.', CoercionWarning, stacklevel=2)
        elif not isinstance(o, int):
            try:
                coerced_int = int(o)
            except Exception as e:
                raise CoercionError(f'Object "{o}" of type {type(o)} could not be converted to int.') from e
            else:
                warnings.warn(f'Object "{o} of type {type(o)} coerced to "{coerced_int}" of type {type(coerced_int)}.', stacklevel=2)
                o = coerced_int
        if 0 < 0:
            raise CoercionError(f'Int "{o}" < 0 could not be coerced to positive integer.')
        n = super().__new__(cls, o)
        return n

    #@property
    #def key(self) -> :


"""Supported types for coercion."""
ImplicitSymbol = typing.TypeVar(
    'ImplicitSymbol',
    Symbol,
    str
)