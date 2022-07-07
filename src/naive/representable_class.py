from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import rformats


class Representable:
    """A base class for objects that support representation in multiple formats."""

    def __init__(self, *args, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Args:
            args: N/A.
            kwargs: Representation formats may be passed in kwargs (e.g. ascii=b'a', latex=r'\phi').
        """

        # If a Representable object is passed as the first args or in kwargs,
        # imitate this object's representation.
        representable = None
        if len(args) > 0:
            if isinstance(args[0], Representable):
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
                # TODO: Implement type coercion for all representation formats.
                if arg_key == rformats.ASCII and not isinstance(arg_value, bytes):
                    arg_value = str.encode(arg_value)
                setattr(self, arg_key, arg_value)

    def __str__(self) -> str:
        representation = self.get_representation()
        if not isinstance(representation, str):
            # ASCII (and possibly others in the future) representation,
            # is implemented as a bytes raw string.
            # Conversion is necessary.
            representation = str(representation)
        return representation

    def __repr__(self):
        return self.__str__()

    def get_representation(self, rformat: str = None, *args, **kwargs) -> str:
        """

        Args:
            rformat (str): The representation format.
            args:
            kwargs:

        Returns:
            The object's representation in the representation format.
        """
        if rformat is None:
            rformat = rformats.DEFAULT
        if hasattr(self, rformat):
            return getattr(self, rformat)
        else:
            # UTF-8 is the fail-safe rformat.
            return getattr(self, rformats.UTF8)

    def imitate(self, o: Representable):
        """Imitate the representation of another object."""
        for f in rformats.CATALOG:
            if hasattr(o, f):
                # Imitate the other object's representation in that format
                setattr(self, f, getattr(o, f))
            elif hasattr(self, f):
                # And remove residual representations
                delattr(self, f)

