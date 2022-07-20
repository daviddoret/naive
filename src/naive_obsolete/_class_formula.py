import glyphs
import log
from _class_atomic_variable import AtomicVariable
from _abc_representable import ABCRepresentable
import rformats
from _class_function import Function, FUNCTION, OPERATOR


class Formula(ABCRepresentable):
    """A generic formula.

    *Formulas are syntactically correct expressions in a formalized language_key defined over a signature, a set of variables, and a logics. In this way, formulas are quite similar to terms. Since predicates and logics symbols are included in their inductive definition, they represent truth values instead of sort values, however.*
    -- https://encyclopediaofmath.org/wiki/Formula

    Bibliography:
        * https://encyclopediaofmath.org/wiki/Formula
    """
    def __init__(
            self,
            symbol,
            arguments,
            **kwargs):
        # TODO: Prevent infinite loops in the Boolean Formula Execution Tree.
        self._symbol = symbol
        # TODO: Check that all arguments are also of type BooleanFormula
        # TODO: Check that the right number of arguments are provided for that symbol
        self._arguments = arguments
        super().__init__()


    @property
    def arity(self):
        return self._symbol.arity

    @property
    def arguments(self):
        return self._arguments

    def list_atomic_variables(self):
        l = set()
        for a in self.arguments:
            if isinstance(a, AtomicVariable):
                l.add(a)
            elif isinstance(a, Formula):
                l_prime = a.list_atomic_variables()
                for a_prime in l_prime:
                    l.add(a_prime)
        # To allow sorting and indexing, convert the set to a list.
        l = list(l)
        l.sort()
        return l

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        if isinstance(self.symbol, AtomicVariable):
            return self.symbol.represent(rformat, *args, **kwargs)
        elif isinstance(self.symbol, Function):
            if self.symbol.preferred_call_representation == FUNCTION:
                # f(x,y,z)
                variable_list = ', '.join(map(lambda a: a.represent(), self.arguments))
                return f'{self.symbol.represent(rformat)}{glyphs.parenthesis_left.represent(rformat)}{variable_list}{glyphs.parenthesis_right.represent(rformat)}'
            elif self.symbol.preferred_call_representation == OPERATOR:
                if self.arity == 1:
                    # fx
                    return f'{self.symbol.represent(rformat)}{self.arguments[0].represent(rformat)}'
                elif self.arity == 2:
                    # x f y
                    return f'{self.arguments[0].represent(rformat)}{glyphs.small_space.represent(rformat)}{self.symbol.represent(rformat)}{glyphs.small_space.represent(rformat)}{self.arguments[1].represent(rformat)}'
                else:
                    log.error('arity > 2 is not supported for OPERATOR call representation.', self=self)
            else:
                log.error('Unknown call representation', self=self)
        else:
            log.error('Symbol of unsupported type in formula.', self=self)

    @property
    def symbol(self):
        return self._symbol

