from __future__ import annotations
import warnings


def coerce(o: (None, object), cls: type) -> (None, object):
    """Coerces an object **o** to type **cls**.

    This function is useful to implement single line argument type coercion in functions and methods.

    If **o** is **None**, returns **None**.

    Else if **o** is of type **cls**, returns **o**.

    Else if **o** is not of type **cls**, creates an instance of **cls** by calling its default constructor, i.e. *cls(o)* and raises a *CoercionWarning*.

    Raises a *CoercionError* if the coercion fails.

    The assumption behind **coerce** is that all classes implement a coercive constructor.

    :param o: An object of undetermined type but presumably compatible with **cls**.
    :param cls: A class that implements a coercive constructor.
    :return: **None**, or an object of type **cls**.
    :rtype: (**None**, **object**).
    """

    """A user-defined warning to allow warning filters."""
    class CoercionWarning(UserWarning):
        pass

    """A user-defined error to facilitate troubleshooting."""
    class CoercionError(Exception):
        pass

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
            warnings.warn(
                f'Object "{o}" of type {type(o)} was coerced to object "{coerced_o}" of type {cls}.',
                CoercionWarning,
                stacklevel=2)
        return cls(o)



