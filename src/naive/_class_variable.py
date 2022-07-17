from _class_variable_base_name import VariableBaseName, CoercibleVariableBaseName
from _class_variable_indexes import VariableIndexes
from _class_variable_exponent import VariableExponent
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_coerce import coerce
from _function_coerce_from_kwargs import coerce_from_kwargs
from _function_flatten import flatten
from _function_superscriptify import superscriptify
from _function_subscriptify import subscriptify
import rformats
import keywords


class Variable(ABCRepresentable):
    """A mathematical variable object.

     A variable is defined as an element that may be defined by a defining object.

    The representation of a variable is composed of a variable base_name,
    conditionally followed by variable indexes.
    """

    def __init__(
            self,
            #source = None,
            base_name: CoercibleVariableBaseName = None,
            indexes: VariableIndexes = None,
            exponent: VariableExponent = None,
            **kwargs):
        """Initializes a variable.

        Kwargs:
            base_name (VariableBaseName): The variable base_name (cf. class :class:´VariableBase´).
            indexes: The variable indexes if it has any (cf. class :class:´VariableIndexes´).
            exponent: The variable exponent it it has one (cf. class :class:´VariableExponent´).
        """

        ## Implicit coercion from source argument.
        #if source is not None:
        #    if isinstance(source, str):
        #        base_name = source  # This is subsequently coerced to VariableBaseName.
        #        # TODO: Enrich this constructor to split indexes from XYZ123
        #    # TODO: Add a constructor that copies a Variable object.

        # Type coercion.
        base_name = coerce(base_name, VariableBaseName)
        indexes = coerce(indexes, VariableIndexes)
        exponent = coerce(exponent, VariableExponent)

        # Set properties.
        self._base_name = base_name
        self._indexes = indexes
        self._exponent = exponent

        super().__init__(**kwargs)

    @property
    def base_name(self) -> VariableBaseName:
        return self._base_name

    @property
    def indexes(self) -> VariableIndexes:
        return self._indexes

    @property
    def exponent(self) -> VariableExponent:
        """The variable exponent.

        This property provides support for n-ary cartesian cross products.

        Returns:
            (None, VariableExponent): The variable exponent.
        """
        return self._exponent

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # TODO: Minor bug: only digits are currently supported by subscript().
        return represent(self.base_name, rformat) + \
               subscriptify(represent(self._indexes, rformat), rformat) + \
               superscriptify(represent(self._exponent, rformat), rformat)
