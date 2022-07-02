from __future__ import annotations

import logging


class NaturalNumber0(int):
    """A class that behaves similarly :math:`n \\in \\mathbb{N}_0`

    The class constructor aggressively coerces its input and raises a warning in non-obvious situations.

    Limitation: the natural number maximum is obviously bounded by the computing environment.
    """
    def __new__(cls: type, o: (None, object)) -> NaturalNumber0:
        """Instantiates a NaturalNumber0.

        Coerces **o** to **NaturalNumber0** and raises a warning in ambiguous situations.

        Args:
            o (object): A source object from which to infer the vector.
            size (int): (Conditional) The size of the vector. Warning: if **o** comprises more elements than **size**, the superfluous elements are truncated with a warning.
            default_value (bool, int): (Conditional) If elements must be populated to reach size, the default value of these new elements.
        """
        if o is None:
            o = 0
            logging.warning()
            # When no source object is passed to the constructor,
            # or alternatively if o=None is passed to the constructor,
            # this is interpreted as "I want an empty set, please".
            o = []
        o = flatten(o)  # Incidentally assure that isinstance(obj) == list.
        if size is not None:
            missing_elements = size - len(o)
            default_value = bool(default_value)
            o.extend([default_value] * missing_elements)
            if len(o) > size:
                # This situation only arises if o was too large from the very beginning
                logging.warning(f'')
                o = o[: size]
        o = np.asarray(o, dtype=bool)
        o = np.asarray(o).view(cls)  # Re-type the instance
        return o