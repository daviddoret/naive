from _abc_representable import ABCRepresentable
from _class_persisting_representable import PersistingRepresentable


class VariableBase(PersistingRepresentable):
    """A variable base is the first component of a variable name."""

    def __init__(self, representable: (None, ABCRepresentable) = None, *args, **kwargs):
        # TODO: Assure that the representable is a word or glyph. We don't want an indexed variable or other inadequate construction to be used a variable base.
        super().__init__(representable, *args, **kwargs)


