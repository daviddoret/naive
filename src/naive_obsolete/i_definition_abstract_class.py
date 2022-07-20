from abc import ABC, abstractmethod
from i_defined_element_abstract_class import ISymbolDefinedElement
from i_defining_element_abstract_class import ISymbolDefiningElement


class ISymbolDefinition(ABC):
    """An abstract class for symbol definition objects that link defined elements to defining elements."""

    @property
    @abstractmethod
    def defined_element(self) -> ISymbolDefinedElement:
        """The element that the defining element defines."""

    @property
    @abstractmethod
    def defining_element(self) -> ISymbolDefiningElement:
        """The element that defines the defined element."""
