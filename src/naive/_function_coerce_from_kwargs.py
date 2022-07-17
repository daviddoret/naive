from __future__ import annotations
from _function_coerce import coerce


def coerce_from_kwargs(key: str, cls: type, **kwargs):
    """Coerces a **kwargs** argument to type **cls**.

    Args:
        key (str): The argument keyword.
        cls (type): The desired type.
        kwargs: The original keyword arguments.

    Returns:
        **cls**: None or the coerced argument.
    """
    arg = kwargs.get(key) if key in kwargs else None
    arg = coerce(arg, cls)
    return arg





