import typing
from _class_function import Function
from _class_set import Set
from _class_function_base_name import FunctionBaseName
from _ba_class_boolean_domain import boolean_domain


class BooleanFunction(Function):

    def __init__(
            self,
            arity: int,
            domain: Set,
            algorithm: typing.Callable,
            base_name: FunctionBaseName,
            indexes = None,
            **kwargs):
        """Initializes a function."""

        codomain = boolean_domain

        super().__init__(
            arity=arity,
            domain=domain,
            codomain=codomain,
            algorithm=algorithm,
            base_name=base_name,
            indexes=indexes,
            **kwargs
        )
