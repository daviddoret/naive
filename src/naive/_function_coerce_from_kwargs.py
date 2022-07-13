from __future__ import annotations
from _function_coerce import coerce


def coerce_from_kwargs(key: str, cls: type, **kwargs) -> (None, object):
    arg = kwargs.get(key) if key in kwargs else None
    return coerce(arg, cls)




