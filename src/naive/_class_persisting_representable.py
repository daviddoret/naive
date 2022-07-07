from __future__ import annotations
from _abc_representable import ABCRepresentable
import rformats


class PersistingRepresentable(ABCRepresentable):
    """A helper class for objects that support representation in multiple formats by storing representations in object properties."""

    def __init__(self, representable: (None, ABCRepresentable) = None, *args, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Args:
            args: N/A.
            kwargs: Representation formats may be passed in kwargs (e.g. ascii='phi', latex=r'\phi').
        """
        self._representations = {}

        super().__init__(*args, **kwargs)


        # If a PersistingRepresentable object was passed as argument,
        # imitate this object'representation representation.
        if representable is not None:
            self.imitate(representable)

        # If representations are provided in specific formats,
        # store these representations.
        # Note that these get priority over above imitation.
        for arg_key, arg_value in kwargs.items():
            if arg_key in rformats.CATALOG:
                # This is a representation format.
                if not isinstance(arg_value, str):
                    # TODO: In future development, if images or other media are supported, reconsider this.
                    arg_value = str(arg_value)
                self._representations[arg_key] = arg_value

    def get_representation(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object'representation representation in the desired format.

        Args:
            rformat (str): The representation format.
            args:
            kwargs:

        Returns:
            The object'representation representation in the representation format.
        """
        if rformat is None:
            rformat = rformats.DEFAULT
        if rformat in self._representations:
            return self._representations[rformat]
        elif rformats.UTF8 in self._representations:
            # We fall back on UTF-8
            return self._representations[rformats.UTF8]
        else:
            raise ValueError(f'PersistingRepresentable object has no representations in {rformat} nor {rformats.UTF8}.')

    def imitate(self, o: ABCRepresentable):
        """Imitate the representation of another object."""
        for rformat in rformats.CATALOG:
            # TODO: Minor design flaw: this process will also copy unsupported properties that default to UTF-8.
            self._representations[rformat] = o.get_representation(rformat)

