import abc
import typing


class ABCRepresentable(abc.ABC):
    """An abstract class for objects that support representation in multiple formats.

    See also:
        * :class:`PersistingRepresentable` class.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        # TODO: For future development, if images or other media are supported, the output of get_presentation() will need to be converted to text.
        return self.represent()

    def __repr__(self):
        return self.__str__()

    @abc.abstractmethod
    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object's representation in the desired format.

        Args:
            rformat (str): The representation format.
            args:
            kwargs:

        Returns:
            The object's representation in the desired format.
        """
        raise NotImplementedError('Abstract method must be implemented in subclass.')


"""Safe types for type coercion."""
CoercibleABCRepresentable = typing.TypeVar(
    'CoercibleABCRepresentable',
    ABCRepresentable,
    bytes, # Support for raw ASCII strings.
    str
)

