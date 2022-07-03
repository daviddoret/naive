from __future__ import annotations
import typing
import warnings
from src.naive.coercion_warning import CoercionWarning
from src.naive.coerce import coerce
from src.naive.forbidden_operation_error import ForbiddenOperationError


class BinaryVariable:
    """A mutable binary variable.

    Alias: :data:`naive.BV`

    The objective of this class is to approach the behavior of :math:`b \\in \\mathbb{B}` in mathematics.

     Example:

         .. jupyter-execute::

             import naive
             b1 = naive.BV(False)
             b2 = naive.BV(True)
             print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')
             b2.bool = True
             print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')

    Notes:
        The python :std:doc:type:`bool` native type cannot be subclassed.
        To implement a bool-like class, :std:doc:meth:`__bool__` method is implemented.

    Bibliography:
        * https://docs.python.org/3/reference/datamodel.html#object.__bool__
        * https://stackoverflow.com/questions/2172189/why-i-cant-extend-bool-in-python
    """

    def __init__(self, o: BinaryValueInput):
        """Instantiates a **BinaryValue**.

         The class constructor coerces its input.
         It issues a **CoercionWarning** in ambiguous situations.
         It raises a **CoercionError** if type coercion fails.

         Args:
             o (BinaryValueInput): A source object from which to instantiate the **BinaryValue**.

         Returns:
             BinaryVariable: A new binary value.

         Raises:
             CoercionWarning: If ambiguous type coercion was necessary.
             CoercionError: If type coercion failed.

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

    def __bool__(self):
        """Provides support for implicit and explicit (i.e. ``bool(x)``) conversions to :std:doc:type:`bool`.

        :return: bool
        """
        return self._inner_bool

    def __eq__(self, other: BinaryValueInput) -> bool:
        """Provides explicit support for equality.

        Even though all python objects are implicitly convertible to bool (calling :std:doc:meth:`__bool__`),
        we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BinaryValue** which issues warnings and raises exceptions as necessary.

        Args:
            other(BinaryValueInput): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BinaryVariable)
        return bool(self) == bool(other)

    @property
    def bool(self):
        """Get/set property

        **BinaryValue** is mutable RESUME HERE
        """
        return self._inner_bool

    @bool.setter
    def bool(self, b: BinaryValueInput):
        self._inner_bool = b

    @bool.deleter
    def bool(self):
        raise(ForbiddenOperationError('Come on... Why would you delete this property?'))



"""This :type:`typing.TypeVar` lists allowed types for implicit type coercion."""
BinaryValueInput = typing.TypeVar(
    'BinaryValueInput',
    BinaryVariable,
    bool,
    int
)