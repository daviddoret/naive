from __future__ import annotations
from abc import ABC, abstractmethod
import warnings
from .coercion_error import CoercionError




class Scopable(ABC):
    """A symbol that is scopable constitutes a scope and may contain variables."""

    def __init__(self):
        self.scope = {}


class Variable:
    def __init__(self, base_name, indexes=None, parent_scope=(None, Variable)):
        self.base_name = sanitize_variable_base_name(base_name)
        self.indexes = indexes
        if indexes is None:
            self.indexed_name = self.base_name
        else:
            self.indexed_name = self.base_name + ','.join(map(str, indexes))



class Natural1IndexedVariableScope(Scope):
    """A scope of variables ."""
    def __init__(self, variable_name):
        super().__init__()



