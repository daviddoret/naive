# Bibliography
# - https://stackoverflow.com/questions/798442/what-is-the-correct-or-best-way-to-subclass-the-python-set-class-adding-a-new
# - https://docs.python.org/3/library/collections.abc.html#collections.abc.Set
import binary_vector
import output
import const
import collections
import itertools
import collections.abc
import mstr


DEFAULT_PREFIX = 'a'


class Atom(str):
    _latex_math = ''

    def __new__(cls, unicode, latex_math=None):
        if latex_math is None:
            latex_math = f'\\text{{{unicode}}}'
        new_instance = str.__new__(cls, unicode)
        new_instance._latex_math = latex_math
        return new_instance

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


class AtomSet(
    collections.abc.Hashable,
    collections.abc.Set,
):
    """A set (small) finite set of atoms

    Desirable requirements:
    - Atoms must be unique
    - Atoms are of python type Atom
    - Order must be stable to allow the reference of Labels by their indices and the usage of indicator (incidence) vectors
    - The objects should be mutable during design-time and immutable during model-checking time
    """

    def __init__(self, source=None, iterable=None, n=None, prefix=DEFAULT_PREFIX, index_start=0):
        self._array = []
        if source is not None and isinstance(source, collections.abc.Iterable):
            self.generate_from_iterable(iterable=source)
        elif iterable is not None and isinstance(iterable, collections.abc.Iterable):
            self.generate_from_iterable(iterable=iterable)
        elif source is not None and isinstance(source, int):
            self.generate_from_range(n=source, prefix=prefix, index_start=index_start)
        elif n is not None and isinstance(n, int):
            self.generate_from_range(n=n, prefix=prefix, index_start=index_start)

    def __contains__(self, item):
        return item in self._array

    def __eq__(self, other):
        if not isinstance(other, AtomSet):
            other = AtomSet(other)
        print(f'{self} == {other}')
        return self._array == other._array

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._array[item]
        elif isinstance(item, str):
            # Supports both str and Atom
            return self._array[self.index(item)]
        raise TypeError('Unsupported item type')

    def __hash__(self):
        return hash(self._array)

    def __iter__(self):
        return iter(self._array)

    def __len__(self):
        return len(self._array)

    def __repr__(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())

    def __str__(self):
        return self.__repr__()

    def _synchronize_index(self):
        """This private method is called internally
        whenever a mutation occurs, to assure that:
        - the internal array contains only unique values
        - the internal array is ordered"""
        self._array = sorted(set(self._array))

    def _append(self, other):
        """Add an item to the set.
        Does not assure that the item is of type MultiFormatString.
        Does not assure that the index is synchronized."""
        self._array.append(other)

    def append(self, other):
        """Add an item to the set.
        Assure that the item is of type MultiFormatString.
        Assure that the index is synchronized."""
        self._append(Atom(other))
        self._synchronize_index()

    def check_consistency(self):
        # To the contrary to state space, label space can be empty.
        return True

    def copy(self):
        """Return a copy of itself"""
        return AtomSet(self._array)

    def discard(self, other):
        # Removing an element from the set does not modify its order
        # but it modifies the consecutive element indices
        self._array.pop(other)

    def generate_from_range(self, n: int = 3, prefix: str = DEFAULT_PREFIX, index_start: int = 0):
        """Generate n elements, prefixed and numbered"""
        for e in range(index_start, index_start + n):
            self._append(Atom(f'{prefix}{e}', f'{prefix}_{{{e}}}'))
        self._synchronize_index()

    def generate_from_iterable(self, iterable: collections.abc.Iterable):
        """Generate elements for every element in the source iterable object"""
        for e in iterable:
            self._append(Atom(e))
        self._synchronize_index()

    def get_dimension_1(self):
        return len(self)

    def get_incidence_vector(self, iterable):
        """Return the incidence vector of the intersection of this set with another set,
        index positions being expressed in relation to this set.

        Bibliography
         - https://en.wikipedia.org/wiki/Indicator_vector
        """
        indicator_vector = binary_vector.BinaryVector(size=len(self))
        for e in iterable:
            e_index = self.index(e)
            indicator_vector[e_index] = 1
        return indicator_vector

    def get_subset(self, incidence_vector):
        return AtomSet(itertools.compress(self._array, incidence_vector))

    def index(self, x):
        return self._array.index(x)

    def to_latex_math(self, direction=const.OUTPUT_HORIZONTAL_DIRECTION):
        """Return a LaTeX matrix representation"""
        if direction == const.OUTPUT_HORIZONTAL_DIRECTION:
            return self.to_latex_math_h()
        elif direction == const.OUTPUT_HORIZONTAL_DIRECTION:
            return self.to_latex_math_v()
        else:
            raise ValueError('Invalid output direction')

    def to_latex_math_h(self):
        """Return a LaTeX horizontal vector representation"""
        content = ', \\; '.join([e.latex_math for e in self._array])
        latex = f'\\left\\{{ {content} \\right\\}}'
        return latex

    def to_latex_math_v(self):
        """Return a LaTeX vertical vector representation"""
        content = ' \\\\ '.join([e.latex_math for e in self._array])
        latex = f'\\begin{{Bmatrix}} {content} \\end{{Bmatrix}}'
        return latex

    # def to_set(self):
    #    """Return a shallow copy of the internal set"""
    #    return set(self._array)

    def to_output_format(self):
        if output.OUTPUT_MODE == output.OUTPUT_LATEX_MATH:
            return self.to_latex_math()
        elif output.OUTPUT_MODE == output.OUTPUT_UNICODE:
            return self.to_unicode()
        else:
            raise NotImplementedError('Unknown output mode')

    def to_unicode(self):
        content = ', '.join([s.unicode for s in self._array])
        return f'{{{content}}}'

    def output(self):
        output.output(self.to_output_format())
        return len(super())
