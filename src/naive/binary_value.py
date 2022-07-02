from __future__ import annotations
import typing
import warnings
from .coercion_warning import CoercionWarning
from .coerce import coerce


class BinaryValue:
    """A class that behaves similarly to :math:`b \\in \\mathbb{B}`.

    Alias: :data:`naive.BV`

    Notes:
        The python :type:`bool` native type cannot be subclassed.
        The solution consists in implementing the :type:`__bool__` method.

    Bibliography:
        * https://docs.python.org/3/reference/datamodel.html#object.__bool__
        * https://stackoverflow.com/questions/2172189/why-i-cant-extend-bool-in-python
    """

    def __init__(self, o: BinaryValueInput):
        """Instantiates a **BinaryValue**.

         The class constructor makes a best effort at coercing its input. It issues a **CoercionWarning** in ambiguous situations. It raises a **CoercionError** if type coercion fails.

         Args:
             o (object): A source object from which to instantiate the **BinaryValue**.

         Returns:
             BinaryValue: A new binary value.

         Raises:
             CoercionWarning: If ambiguous type coercion was necessary.
             CoercionError: If type coercion failed.

         Example:

             .. jupyter-execute::

                 import naive
                 b = naive.BV(False)
                 print(type(b))
                 print(b)

         """

        if o is None:
            o = 0
            warnings.warn(f'None coerced to 0.', CoercionWarning, stacklevel=2)
        elif not isinstance(o, bool):
            coerced_bool = bool(o)
            warnings.warn(f'Object "{o} of type {type(o)} coerced to "{coerced_bool}" of type {type(coerced_bool)}.',
                          stacklevel=2)
            o = coerced_bool
        self._inner_bool = o

    def __eq__(self, other: BinaryValueInput) -> bool:
        """

        :param other:
        :return:
        """
        other = coerce(other, BinaryValue)
        return self == other

"""This :type:`typing.TypeVar` lists allowed types for implicit type coercion."""
BinaryValueInput = typing.TypeVar(
    'BinaryValueInput',
    BinaryValue,
    bool,
    int
)