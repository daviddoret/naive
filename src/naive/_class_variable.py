from _class_variable_base_name import VariableBaseName
from _class_variable_indexes import VariableIndexes
from _class_variable_power import VariablePower
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_coerce import coerce
from _function_flatten import flatten
import rformats


class Variable(ABCRepresentable):
    """A mathematical variable object.

     A variable is defined as an element that may be defined by a defining object.

    The representation of a variable is composed of a variable base_name,
    conditionally followed by variable indexes.
    """

    def __init__(self, base_name: VariableBaseName, *args, power = None):
        """Initializes a variable.

        Args:
            base_name (VariableBaseName): The variable base_name (cf. class :class:´VariableBase´).
            *args: Variable length list of index elements (cf. class :class:´VariableIndexes´).
        """
        self._base_name = coerce(base_name, VariableBaseName)
        self._power = coerce(power, VariablePower)
        #power = None
        #if 'power' in kwargs:
        #    power = kwargs.get('power')
        #self._power = coerce(power, VariablePower)
        f = flatten(*args)
        if f is not None and f != [None]:
            self._indexes = coerce(f, VariableIndexes)
        else:
            self._indexes = None
        super().__init__(base_name, *args, power)

    @property
    def base_name(self) -> VariableBaseName:
        return self._base_name

    @property
    def indexes(self) -> VariableIndexes:
        return self._indexes

    @property
    def power(self) -> VariablePower:
        return self._power

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # TODO: Minor bug: only digits are currently supported by subscript().
        return represent(self._base_name, rformat) + \
               represent(self._indexes, rformat) + \
               represent(self._power, rformat)
