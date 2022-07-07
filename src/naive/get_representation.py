from _abc_representable import ABCRepresentable
import rformats


def get_representation(o: object, rformat: str = None, *args, **kwargs) -> str:
    """Get the object's representation in the desired format.

    If **o** is ABCRepresentable, return **o**.get_representation().
    Else, return str(**o**).

    Args:
        o (object): The object to be represented.
        rformat (str): The representation format.

    Returns:
        The object's representation, if support in the desired format.
    """
    if rformat is None:
        rformat = rformats.DEFAULT
    if isinstance(o, ABCRepresentable):
        return o.get_representation(rformat, *args, **kwargs)
    else:
        return str(o)
