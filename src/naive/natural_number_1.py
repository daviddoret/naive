from __future__ import annotations
import warnings
from src.naive.coercion_error import CoercionError
from src.naive.coercion_warning import CoercionWarning


class NaturalNumber1(int):
    """Natural numbers (ℕ.

    Alias: :data:`naive.NN1`

    Notes:
        Limitation: the natural number maximum is obviously bounded by the computing environment.


    """
    def __new__(cls: type, o: (None, object) = None) -> NaturalNumber1:
        """Instantiates a **NaturalNumber1**.

        The class constructor makes a best effort at coercing its input. It issues a **CoercionWarning** in ambiguous situations. It raises a **CoercionError** if type coercion fails.

        Args:
            o (object): A source object from which to instantiate the **NaturalNumber1**.

        Returns:
            NaturalNumber1: A new natural number.

        Raises:
            CoercionWarning: If ambiguous type coercion was necessary.
            CoercionError: If type coercion failed.

        Example:

            .. jupyter-execute::

                import naive
                n = naive.NN1(17)
                print(type(n))
                print(n)

        """

        if o is None:
            o = 1
            warnings.warn(f'None coerced to 1.', CoercionWarning, stacklevel=2)
        elif not isinstance(o, int):
            try:
                coerced_int = int(o)
            except Exception as e:
                raise CoercionError(f'Object "{o}" of type {type(o)} could not be converted to int.') from e
            else:
                warnings.warn(f'Object "{o} of type {type(o)} coerced to "{coerced_int}" of type {type(coerced_int)}.', stacklevel=2)
                o = coerced_int
        if o < 1:
            raise CoercionError(f'Int "{o}" < 1 could not be coerced.')
        n = super().__new__(cls, o)
        return n



