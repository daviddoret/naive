from naive._class_persisting_representable import PersistingRepresentable


class Glyph(PersistingRepresentable):
    """A glyph is an elemental representation item."""

    def __init__(self, *args, **kwargs):
        """Initializes a Glyph object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)



