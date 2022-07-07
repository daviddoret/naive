from i_representable_abstract_class import IRepresentable


class Glyph(IRepresentable):
    """A glyph is an elemental representation item."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

