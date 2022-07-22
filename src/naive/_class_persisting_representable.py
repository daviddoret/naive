from __future__ import annotations
import typing
from _abc_representable import ABCRepresentable
import rformats
from _function_coerce import coerce


class PersistingRepresentable(ABCRepresentable):
    """A helper class for objects that support representation in multiple formats by storing representations in
    object properties."""

    def __init__(self, source=None, source_representable=None, source_string=None, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Kwargs:
            source_representable (ABCRepresentable): A source source_representable object whose representation should be imitated.
            source_string (source_string): A source object that may be converted to **source_string** to get a UTF-8 representation.
            ...: Representation formats may be passed in kwargs (e.g. usascii='phi', latex=r'\phi').
        """
        if source is not None:
            # Support for implicit conversion during type coercion.
            if isinstance(source, ABCRepresentable):
                source_representable = source
            else:
                source_string = str(source)

        source_representable = coerce(source_representable, ABCRepresentable)
        source_string = coerce(source_string, str)

        self._representations = {}

        if source_representable is not None:
            # If a PersistingRepresentable object was passed as argument,
            # imitate this object's representations.
            self.imitate(source_representable)
        elif source_string is not None:
            # Otherwise, we must assume it was a string or other
            # string-like Unicode representation.
            self._representations[rformats.UTF8] = source_string

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

        super().__init__(**kwargs)

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object's representation in a supported format.

        Args:
            rformat (str): A representation format.
            args: For future use.
            kwargs: For future use.

        Returns:
            The object's representation in the requested format.
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
            self._representations[rformat] = o.represent(rformat)


"""Safe types for type coercion."""
CoerciblePersistingRepresentable = typing.TypeVar(
    'CoerciblePersistingRepresentable',
    ABCRepresentable,
    bytes,  # Support for raw USASCII strings.
    PersistingRepresentable,
    str
)
