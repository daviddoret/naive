import warnings
import binary_vector
import output
import const
import collections
import itertools
import collections.abc
import mstr
import typing

DEFAULT_PREFIX = 's'

# Pre-declare the typing variables to prevent NameErrors:
StateInput = None
StateOutput = None


class IV(binary_vector.BinaryVector):
    def __init__(self, v=None, size=None, value=None):
        if isinstance(v, IV):
            # The IV type couldn't be expressly managed in the parent class
            v = v.to_bool_numpy_array()
        super().__init__(v, size, value)


class State(str):
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
        return State(self.unicode, self.latex_math)

    @property
    def latex_math(self):
        return self._latex_math

    @property
    def unicode(self):
        return str.__str__(self)


class StateSet(
    collections.abc.Hashable,
    collections.abc.Set,
):
    """A set (small) finite set of states

    Desirable requirements:
    - Atoms must be unique
    - Atoms are of python type State
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
        if not isinstance(other, StateSet):
            other = StateSet(other)
        print(f'{self} == {other}')
        return self._array == other._array

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._array[item]
        elif isinstance(item, str):
            # Supports both str and State
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
        self._append(State(other))
        self._synchronize_index()

    def check_consistency(self):
        if not len(self) > 0:
            warnings.warn('CONSISTENCY WARNING: A state space must contain at least one state: not len(self) > 0')
            return False
        return True

    def copy(self):
        """Return a copy of itself"""
        return StateSet(self._array)

    def discard(self, other):
        # Removing an element from the set does not modify its order,
        # but it modifies the consecutive element indices
        self._array.pop(other)

    def generate_from_range(self, n: object = 3, prefix: str = DEFAULT_PREFIX, index_start: object = 0):
        """Generate n elements, prefixed and numbered"""
        for e in range(index_start, index_start + n):
            self._append(State(f'{prefix}{e}', f'{prefix}_{{{e}}}'))
        self._synchronize_index()

    def generate_from_iterable(self, iterable):
        """Generate elements for every element in the source iterable object"""
        for e in iterable:
            self._append(State(e))
        self._synchronize_index()

    def get_dimension_1(self):
        return len(self)

    def get_set(self, incidence_vector):
        """Return the state set corresponding to an incidence vector"""
        return StateSet(itertools.compress(self._array, incidence_vector))

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

    def to_mstr(self) -> mstr.MStr:
        return mstr.MStr(self.to_unicode(), self.to_latex_math())

    def output(self):
        output.output(self.to_output_format())
        return len(super())


# In order to develop flexible python methods that may
# receive many different state or state set representations,
# the TypeVar StateInput is defined as following.
# Reference: https://peps.python.org/pep-0484/
StateInput = typing.TypeVar(
    'StateInput',
    str,  # By state name
    int,  # By state index position in the model state set
    State,  # By single state object
    StateSet,  # By state set
    binary_vector.BinaryVector,  # By incidence vector linked to the model state set
    IV  # By incidence vector linked to the model state set
)

# In order to develop flexible python methods that may
# receive many different state or state set representations,
# the TypeVar StateInput is defined as following.
# Reference: https://peps.python.org/pep-0484/
StateOutput = typing.TypeVar(
    'StateOutput',
    StateSet,  # By state set
    IV  # By incidence vector linked to the model state set
)


def get_iv_from_idx(base: StateSet, index_position: int) -> IV:
    """Return the incidence vector of the set that contains the state with that index position"""
    iv = IV(size=base.get_dimension_1(), value=0)
    iv[index_position] = 1
    return iv


def get_iv_from_state(base: StateSet, s: typing.Union[str, State]) -> IV:
    """Return the incidence vector of the set that contains that state"""
    index_position = base.index(s)
    return get_iv_from_idx(base, index_position)


def get_iv_from_stateset(base: StateSet, s: collections.abc.Iterable) -> IV:
    """Return the incidence vector of a state set"""
    iv = IV(size=len(base), value=0)
    for e in s:
        e_index = base.index(e)
        iv[e_index] = 1
    return iv


def get_iv(base: StateSet, s: StateInput) -> StateOutput:
    """Return the incidence vector of a state or state set expressed with various python types

    Mapping rules to determine the output type from the input type:
    INPUT TYPE:     |   OUTPUT TYPE:    |   CATEGORY:
    str             |   StateSet        |   name
    State           |   StateSet        |   name
    StateSet        |   StateSet        |   name
    int             |   IV              |   index
    BinaryVector    |   IV              |   index
    IV              |   IV              |   index
    """

    base = base if isinstance(base, StateSet) else StateSet(base)

    output_value = None
    output_type = IV
    # First, prepare the incidence vector
    if isinstance(s, int):
        output_value = get_iv_from_idx(base, s)
    elif isinstance(s, binary_vector.BinaryVector):
        # This is already an incidence vector
        output_value = IV(s)
    elif isinstance(s, IV):
        # This is already an incidence vector
        output_value = s.copy()
    elif isinstance(s, collections.abc.Iterable) and all(isinstance(e, bool) for e in s):
        # [True, False, True, ...]
        output_value = IV(s)
    elif isinstance(s, collections.abc.Iterable) and all(isinstance(e, int) for e in s):
        # [1, 0, 1, ...]
        output_value = IV(s)
    elif isinstance(s, State) or isinstance(s, str):
        # s
        output_value = get_iv_from_state(base, s)
        output_type = StateSet
    elif isinstance(s, StateSet):
        # S
        output_value = get_iv_from_stateset(base, s)
        output_type = StateSet
    elif isinstance(s, collections.abc.Iterable) and all(isinstance(e, str) for e in s):
        # ['s1', 's2', ...]
        output_value = get_iv_from_stateset(base, s)
        output_type = StateSet
    elif isinstance(s, collections.abc.Iterable) and all(isinstance(e, State) for e in s):
        # [s1, s2, ...]
        output_value = get_iv_from_stateset(base, s)
        output_type = StateSet
    else:
        raise TypeError('Unsupported type')
    if not output_type == IV:
        output_value = StateSet(output_value)
