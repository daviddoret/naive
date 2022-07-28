from _class_variable import Variable
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


class AtomicVariable(Variable):
    """The atomic variable class.

    Definition:
    An atomic variable is a variable that is not a phi variable,
    that it is cannot be decomposed into sub-phi.
    One way to understand it is to see it as an unknown variable.
    """
    def __init__(
            self,
            #source = None,
            base_name: CoercibleVariableBaseName = None,
            indexes: VariableIndexes = None,
            exponent: VariableExponent = None,
            **kwargs):
        super().__init__(
            base_name = base_name,
            indexes = indexes,
            exponent = exponent,
            **kwargs)
