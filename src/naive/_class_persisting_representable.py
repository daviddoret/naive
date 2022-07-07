from __future__ import annotations
from _abc_representable import ABCRepresentable
import rformats


class PersistingRepresentable(ABCRepresentable):
    """A helper class for objects that support representation in multiple formats by storing representations in object properties."""

    def __init__(self, *args, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Args:
            args: N/A.
            kwargs: Representation formats may be passed in kwargs (e.g. ascii='phi', latex=r'\phi').
        """

        super().__init__(*args, **kwargs)

        # If a PersistingRepresentable object is passed as the first args or in kwargs,
        # imitate this object's representation.
        representable = None
        if len(args) > 0:
            if isinstance(args[0], ABCRepresentable):
                representable = args[0]
        else:
            if 'representable' in kwargs:
                representable = kwargs['representable']
        if representable is not None:
            self.imitate(representable)

        # If representations are provided in specific formats,
        # store these representations.
        # Note that this takes priority over above imitation.
        for arg_key, arg_value in kwargs.items():
            if arg_key in rformats.CATALOG:
                # This is a representation format.
                if not isinstance(arg_value, str):
                    # TODO: In future development, if images or other media are supported, reconsider this.
                    arg_value = str(arg_value)
                property_name = f'_{arg_key}'
                setattr(self, property_name, arg_value)
                # match arg_key:
                #     case rformats.UTF8:
                #         self.utf8 = arg_value
                #     case rformats.LATEX:
                #         self.latex = arg_value
                #     case rformats.HTML:
                #         self.html = arg_value
                #     case rformats.ASCII:
                #         self.ascii = arg_value
                #     case _:
                #         raise ValueError(f'Unknown format "{arg_value}"')

    def get_representation(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object's representation in the desired format.

        Args:
            rformat (str): The representation format.
            args:
            kwargs:

        Returns:
            The object's representation in the representation format.
        """
        if rformat is None:
            rformat = rformats.DEFAULT
        property_name = f'_{rformat}'
        if hasattr(self, property_name):
            return getattr(self, property_name)
        else:
            # UTF-8 is the fail-safe rformat.
            return getattr(self, rformats.UTF8)

    def imitate(self, o: ABCRepresentable):
        """Imitate the representation of another object."""
        for rformat in rformats.CATALOG:
            # TODO: Minor design flaw: this process will also copy unsupported properties that default to UTF-8.
            setattr(self, f'_{rformat}', o.get_representation(rformat))
        # self.utf8 = o.get_representation(rformats.UTF8)
        # self.latex = o.get_representation(rformats.LATEX)
        # self.html = o.get_representation(rformats.HTML)
        # self.ascii = o.get_representation(rformats.ASCII)

