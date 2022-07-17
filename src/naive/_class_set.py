from __future__ import annotations

import log
from _ba_class_boolean_value import BooleanValue
from _function_coerce_from_kwargs import coerce_from_kwargs
from _function_coerce import coerce
import keywords


class Set:

    def __init__(self, dimensions: int, **kwargs):
        """Set initialization.

        Kwargs:
            dimensions (int): The number of dimensions in the set. Default: 1.
        """
        dimensions = coerce(dimensions, int)
        if dimensions is None:
            log.error('Dimensions is a mandatory set property.')
        self._dimensions = dimensions
        super().__init__()  # TODO: Clarify why we can't just pass **kwargs to object?

    @property
    def dimensions(self):
        # TODO: For the future implementation of NFoldCartesianProduct
        return self._dimensions
