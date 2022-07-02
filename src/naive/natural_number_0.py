from __future__ import annotations

from .coercion_error import CoercionError
from .coercion_warning import CoercionWarning
import warnings


class NaturalNumber0(int):
    """A class that behaves similarly to :math:`n \\in \\mathbb{N}_0`

    The class constructor coerces its input.

    Issues a *CoercionWarning* in ambiguous situations.

    Raises a *CoercionError* if type coercion fails.

    Limitation: the natural number maximum is obviously bounded by the computing environment.
    """
    def __new__(cls: type, o: (None, object) = None) -> NaturalNumber0:
        """Instantiates a **NaturalNumber0**.

        Args:
            o (object): A source object from which to instantiate the **NaturalNumber0**.
        """

        if o is None:
            o = 0
            warnings.warn(f'None coerced to 0.', CoercionWarning, stacklevel=2)
        try:
            coerced_int = int(o)
        except Exception as e:
            raise CoercionError(f'Object "{o}" of type {type(o)} could not be coerced to integer.') from e
        if coerced_int < 0:
            raise CoercionError(f'{coerced_int} < 0 could not be coerced to positive integer.')
        n = super().__new__(cls, coerced_int)
        return n

