import typing
import inspect


import glyphs
import log
from _class_set import Set


from _class_function_base_name import FunctionBaseName
from _class_function_indexes import FunctionIndexes
from _class_variable import Variable
from _class_variable_indexes import VariableIndexes
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_coerce import coerce
from _function_flatten import flatten
import rformats


class Function(ABCRepresentable):
    """A mathematical function.

    The representation of a function is composed of a function base_name,
    conditionally followed by function indexes.
    """

    def __init__(
            self,
            domain: Set,
            codomain: Set,
            algorithm: typing.Callable,
            base_name: FunctionBaseName,
            *args,
            indexes = None,
            **kwargs):
        """Initializes a function.

        Args:
            base_name (VariableBaseName): The variable base_name (cf. class :class:´VariableBase´).
            *args: Variable length list of index elements (cf. class :class:´VariableIndexes´).
        """
        self._domain = coerce(domain, Set)
        self._codomain = coerce(codomain, Set)
        self._algorithm = algorithm  # TODO: Implement algo type properly, then coerce(algorithm, typing.Callable)
        self._base_name = coerce(base_name, FunctionBaseName)
        self._indexes = coerce((*args, indexes), VariableIndexes)
        super().__init__(base_name, *args)

    def __call__(self, *args):
        return self._algorithm(*args)

    @property
    def algorithm(self) -> typing.Callable:
        """A python algorithm able to compute the function's output.

        Returns:
             typing.Callable: A python function.
        """
        # TODO: Implement algorithm as a dedicated class. Then implement friendly representation. Use inspect.getsource(foo) for that.
        return self._algorithm

    @property
    def arity(self):
        """The function's arity.

        The arity of a function is the number of arguments received by that function.
        The arity of the function must be consistent with the dimensions of its domain.

        Returns:
            object: The function's arity.
        """
        return self.domain.dimensions

    @property
    def base_name(self) -> FunctionBaseName:
        return self._base_name

    @property
    def codomain(self) -> Set:
        return self._codomain

    @property
    def domain(self) -> Set:
        return self._domain

    @property
    def indexes(self) -> FunctionIndexes:
        return self._indexes

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # TODO: Minor bug: only digits are currently supported by subscript().
        return represent(self._base_name, rformat) + \
               represent(self._indexes, rformat)

    def represent_declaration(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT

        variable_list = ','.join(map(lambda i: Variable('x', str(i)).represent(), range(1, self.arity + 2)))
        match rformat:
            case rformats.LATEX:
                return f'\\begin{{align*}} {represent(self, rformat)} {represent(glyphs.colon, rformat)} {represent(self.domain, rformat)} &{represent(glyphs.to, rformat)} {represent(self.codomain, rformat)} \\\\ {variable_list} & {represent(glyphs.maps_to, rformat)} {represent(self.algorithm, rformat)} \\end{{align*}}'
            case rformats.UTF8:
                return f'{represent(self, rformat)} {represent(glyphs.colon, rformat)} {represent(self.domain, rformat)} {represent(glyphs.to, rformat)} {represent(self.codomain, rformat)} \n \t {variable_list} {represent(glyphs.maps_to, rformat)} {represent(self.algorithm, rformat)}'
            case rformats.HTML:
                return f'{represent(self, rformat)} {represent(glyphs.colon, rformat)} {represent(self.domain, rformat)} {represent(glyphs.to, rformat)} {represent(self.codomain, rformat)} <br> &emsp; {variable_list} {represent(glyphs.maps_to, rformat)} {represent(self.algorithm, rformat)}'
            case rformats.ASCII:
                return f'{represent(self, rformat)} {represent(glyphs.colon, rformat)} {represent(self.domain, rformat)} {represent(glyphs.to, rformat)} {represent(self.codomain, rformat)} \n \t {variable_list} {represent(glyphs.maps_to, rformat)} {represent(self.algorithm, rformat)}'
            case _:
                log.NaiveError('Unsupported representation format.', rformat=rformat)


F = Function
"""A shorthand notation for class :class:`Function`."""
