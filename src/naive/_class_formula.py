from _class_atomic_variable import AtomicVariable


class Formula:
    """A generic formula.

    *Formulas are syntactically correct expressions in a formalized language defined over a signature, a set of variables, and a logics. In this way, formulas are quite similar to terms. Since predicates and logics symbols are included in their inductive definition, they represent truth values instead of sort values, however.*
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

    @property
    def symbol(self):
        return self._symbol

