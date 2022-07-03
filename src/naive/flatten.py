import typing
import collections.abc as abc


def flatten(*args: object) -> typing.List[typing.Any]:
    """Flatten iterable objects of arbitrary depth.

    This utility function converts embedded lists or multidimensional objects to vectors.

    If x is already a flat list, returns a new list instance with the same elements.

    If x is not iterable, returns an iterable version of x, that is: [x].

    If x is None, returns an empty list, that is [].

    Args:
        x (object): Any object but preferably an iterable object of type: abc.Iterable[typing.Any].

    Returns:
         A flat list.

    """
    flattened = []
    for y in args:
        # Recursive call for sub-structures
        # except strings that are understood as atomic in this context
        if isinstance(y, abc.Iterable) and not isinstance(y, str):
            # We cannot call directly extend to support n-depth structures
            flattened.extend(flatten(*y))
        else:
            flattened.append(y)
    return flattened

