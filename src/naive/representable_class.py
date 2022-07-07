from abc import ABC, abstractmethod
from dataclasses import dataclass
import rformats


class IRepresentable:
    """A base class for objects that support representation in multiple formats."""

    def __init__(self, *args, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Args:
            args: N/A.
            kwargs: Representation formats may be passed in kwargs (e.g. ascii=b'a', latex=r'\phi').
        """
        for arg_key, arg_value in kwargs.items():
            if arg_key in rformats.CATALOG:
                # This is a representation format.
                # TODO: Implement type coercion for all representation formats.
                if arg_key == rformats.ASCII and not isinstance(arg_value, bytes):
                    arg_value = str.encode(arg_value)
                setattr(self, arg_key, arg_value)

    def __str__(self):
        return self.get_representation()

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

