from __future__ import annotations
import typing

from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _abc_representable import ABCRepresentable
from _function_coerce import coerce
import glyphs
import log


class Formula(PersistingRepresentable):

    def __new__(cls, pythonic_value: bool):
        pass

    def __init__(self, pythonic_value: bool):
        pass

F = Formula
"""A shorthand alias for class :class:`BinaryValue`."""

