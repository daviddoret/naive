from __future__ import annotations

from .coercion_error import CoercionError
from .coercion_warning import CoercionWarning
import warnings


class NaturalNumber0(int):
    """A class that behaves similarly to :math:`n \\in \\mathbb{N}_0`.

    Alias: :data:`naive.NN0`

    Notes:
        Limitation: the natural number maximum is obviously bounded by the computing environment.


    """
    def __new__(cls: type, o: (None, object) = None) -> NaturalNumber0:
        """Instantiates a **NaturalNumber0**.

        The class constructor makes a best effort at coercing its input. It issues a **CoercionWarning** in ambiguous situations. It raises a **CoercionError** if type coercion fails.

        Args:
            o (object): A source object from which to instantiate the **NaturalNumber0**.

        Returns:
            NaturalNumber0: A new natural number.

        Raises:
            CoercionWarning: If ambiguous type coercion was necessary.
            CoercionError: If type coercion failed.

        Example:

            .. jupyter-execute::

                import naive
                n = naive.NN0(17)
                print(type(n))
                print(n)

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

