from __future__ import annotations
from _class_boolean_value import BooleanValue
from _function_coerce import coerce


class Set(object):

    def __init__(self, *args, dimensions=None, **kwargs):
        dimensions = coerce(dimensions, int)
        if dimensions is None:
            dimensions = 1
        self._dimensions = dimensions
        super().__init__()

    @property
    def dimensions(self):
        # TODO: For the future implementation of NFoldCartesianProduct
        return self._dimensions
