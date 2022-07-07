from _class_persisting_representable import PersistingRepresentable


class Glyph(PersistingRepresentable):
    """A glyph is an elemental representation item."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

