

class Representation:
    """A representation is an ordered paid (content, representation rformat)."""

    def __init__(self, content: str, format: str):
        self._content = content
        self._format = format

    @property
    def content(self) -> str:
        return self._content

    @property
    def format(self) -> str:
        return self._format

