from __future__ import annotations
import naive.log


def coerce(
        o: (None, object),
        cls: type) -> (None, object):
    """Coerces an object **representation** to type **cls**.

    This function is useful to implement single line argument type coercion for the validation of arguments in functions and methods.

    The assumption behind **coerce** is that all classes implement a coercive constructor.

    Args:
        o (object): An object of undetermined type, but compatible with **cls**.
        cls (type): A class that implements a coercive constructor.

    Returns:
        object: **None**, or an object of type **cls**.

    Raises:
        NaiveWarning: If ambiguous type coercion was necessary.
        NaiveError: If type coercion failed.

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

        1. If **representation** is **None**, returns **None**.

        2. Else if **representation** is of type **cls**, returns **representation**.

        3. Else if **representation** is not of type **cls**, creates an instance of **cls** by calling its default constructor, i.e. ``cls(representation)`` and issue a **NaiveWarning**.


    """
    if o is None:
        return None
    elif isinstance(o, cls):
        # The object is already of the expected type.
        # Return the object itself.
        return o
    else:
        # The object is not of the expected type,
        # we must attempt to force its conversion,
        # by calling the constructor of the desired type,
        # passing it the source object.
        try:
            coerced_o = cls(o)
        except Exception as e:
            naive.log.error(code = naive.log.COERCION_FAILURE, o = o, cls = cls)
        else:
            naive.log.debug(code = naive.log.COERCION_SUCCESS, o = o, cls = cls)
        return cls(o)



