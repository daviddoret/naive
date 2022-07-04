from __future__ import annotations
import typing
import warnings
from src.naive.coercion_warning import CoercionWarning
from src.naive.coerce import coerce
from src.naive.forbidden_operation_error import ForbiddenOperationError
from src.naive.variable import VariableValue
import src.naive.settings as settings


class BinaryValue(VariableValue):
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

    """Class attribute for text representation."""
    class_notation = settings.BINARY_NUMBER_DOMAIN_NOTATION

    def __init__(self, o: CoercibleBinaryValue):
        """Instantiates a **BinaryValue**.

         The class constructor coerces its input.
         It issues a **CoercionWarning** in ambiguous situations.
         It raises a **CoercionError** if type coercion fails.

         Args:
             o (CoercibleBinaryValue): A source object from which to instantiate the **BinaryValue**.

         Returns:
             BinaryValue: A new binary value.

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

    def __eq__(self, other: CoercibleBinaryValue) -> bool:
        """Provides explicit support for equality.

        Even though all python objects are implicitly convertible to bool (calling :std:doc:meth:`__bool__`),
        we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BinaryValue** which issues warnings and raises exceptions as necessary.

        Args:
            other(CoercibleBinaryValue): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BinaryValue)
        result = bool(self) == bool(other) # Explicit conversion is superfluous but clearer
        return result

    def __str__(self):
        if self:
            return settings.BINARY_VALUE_1_NOTATION
        else:
            return settings.BINARY_VALUE_0_NOTATION

    def __repr__(self):
        return str(self)


BV = BinaryValue


"""Safe types for type coercion."""
CoercibleBinaryValue = typing.TypeVar(
    'CoercibleBinaryValue',
    BinaryValue,
    bool,
    int
)
