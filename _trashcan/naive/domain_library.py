"""Mathematical domains management"""
# TODO: Implement domain generators, e.g. for B^1, B^2, B^3, etc.
# TODO: Implement domain / sub-domains relations, e.g. for B^5 subset of B^n.


class Domain:
    """A mathematical domain.

    Sample use cases:
        * Function domain
        * Operator domain
        * Set domain
        * Variable domain
    """
    def __init__(self, unicode_notation):
        self.unicode_notation = str(unicode_notation)

    def __hash__(self):
        return hash(self.unicode_notation)

    def __str__(self) -> str:
        return self.unicode_notation


