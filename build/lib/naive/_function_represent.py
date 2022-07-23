from _abc_representable import ABCRepresentable
import rformats


def represent(o: object, rformat: str = None, *args, **kwargs) -> str:
    """Get the object'representation representation in the desired format.

    If **representation** is None, return an empty string.
    Else if **representation** is ABCRepresentable, return **representation**.get_representation().
    Else, return source_string(**representation**).

    Args:
        o (object): The object to be represented.
        rformat (str): The representation format.

    Returns:
        The object'representation representation, if support in the desired format.
    """
    if o is None:
        # If nothing is passed for representation,
        # we return an empty string to facilitate concatenations.
        return ''
    if rformat is None:
        rformat = rformats.DEFAULT
    if isinstance(o, ABCRepresentable):
        return o.represent(rformat, *args, **kwargs)
    else:
        return str(o)
