from representable_class import Representable


class Glyph(Representable):
    """A glyph is an elemental representation item."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

