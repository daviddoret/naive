

class MStr(str):
    _latex_math = ''

    def __new__(cls, unicode, latex_math=None):
        if latex_math is None:
            latex_math = f'\\text{{{unicode}}}'
        new_instance = str.__new__(cls, unicode)
        new_instance._latex_math = latex_math
        return new_instance

    def __add__(self, o):
        """Concatenates simultaneously the different string formats"""
        return MStr(
            self.unicode + o.unicode,
            self.latex_math + o.latex_math)

    def __repr__(self):
        return self.unicode

    def __str__(self):
        return self.unicode

    def copy(self):
        return Atom(self.unicode, self.latex_math)

    @property
    def latex_math(self):
        return self._latex_math

    @property
    def unicode(self):
        return str.__str__(self)
