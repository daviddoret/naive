from __future__ import annotations
import warnings
from coercion_error import CoercionError
from coercion_warning import CoercionWarning


def coerce(o: (None, object), cls: type) -> (None, object):
    """Coerces an object **o** to type **cls**.

    This function is useful to implement single line argument type coercion for the validation of arguments in functions and methods.

    The assumption behind **coerce** is that all classes implement a coercive constructor.

    Args:
        o (object): An object of undetermined type, but compatible with **cls**.
        cls (type): A class that implements a coercive constructor.

    Returns:
        object: **None**, or an object of type **cls**.

    Raises:
        CoercionWarning: If ambiguous type coercion was necessary.
        CoercionError: If type coercion failed.

    Example:

        .. jupyter-execute::

            # import naive
            n = "5"
            print(n)
            #n_prime = naive.coerce(n, naive.NN0)
            #print(type(n_prime))
            #print(n_prime)

    Notes:
        High-level algorithm:

        1. If **o** is **None**, returns **None**.

        2. Else if **o** is of type **cls**, returns **o**.

        3. Else if **o** is not of type **cls**, creates an instance of **cls** by calling its default constructor, i.e. ``cls(o)`` and issue a **CoercionWarning**.


    """
    if o is None:
        return None
    elif isinstance(o, cls):
        return o
    else:
        try:
            coerced_o = cls(o)
        except Exception as e:
            raise CoercionError(f'Object "{o}" of type {type(o)} could not be coerced to type {cls}.') from e
        else:
            warnings.warn(f'Object "{o}" of type {type(o)} was coerced to object "{coerced_o}" of type {cls}.', CoercionWarning, stacklevel=2)
        return cls(o)



