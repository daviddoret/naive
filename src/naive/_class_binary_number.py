from __future__ import annotations
import typing
import warnings
from _exception_coercion_warning import CoercionWarning
from _function_coerce import coerce
from _class_domain import Domain
import notation
import domains


class BinaryNumber:
    """A mutable binary variable.

    Alias: :data:`BN`

    The objective of this class is to approach the behavior of :math:`b \\in \\mathbb{B}` in mathematics.

     Example:

         .. jupyter-execute::

             import naive
             b1 = naive.BN(False)
             b2 = naive.BN(True)
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
    class_notation = notation.BINARY_NUMBER_DOMAIN_NOTATION

    def __init__(self, o: CoercibleBinaryNumber):
        """Instantiates a **BinaryValue**.

         The class constructor coerces its input.
         It issues a **CoercionWarning** in ambiguous situations.
         It raises a **CoercionError** if type coercion fails.

         Args:
             o (CoercibleBinaryNumber): A source object from which to instantiate the **BinaryValue**.

         Returns:
             BinaryNumber: A new binary value.

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

    def __eq__(self, other: CoercibleBinaryNumber) -> bool:
        """Provides explicit support for equality.

        Even though all python objects are implicitly convertible to bool (calling :std:doc:meth:`__bool__`),
        we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BinaryNumber** which issues warnings and raises exceptions as necessary.

        Args:
            other(CoercibleBinaryNumber): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BinaryNumber)
        result = bool(self) == bool(other) # Explicit conversion is superfluous but clearer
        return result

    def __str__(self):
        if self:
            return notation.BINARY_VALUE_1_NOTATION
        else:
            return notation.BINARY_VALUE_0_NOTATION

    def __repr__(self):
        return str(self)

    @property
    def domain(self) -> Domain:
        return domains.b


"""A shorthand alias for class :class:`BinaryNumber`."""
BN = BinaryNumber


"""Supported types for coercion to class :class:`BinaryNumber`."""
CoercibleBinaryNumber = typing.TypeVar(
    'CoercibleBinaryNumber',
    BinaryNumber,
    bool,
    int
)



