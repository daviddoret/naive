from __future__ import annotations
import collections.abc
import logging
import threading
import graphviz
import typing
import abc
from textx import metamodel_from_file, metamodel_from_str
import pkg_resources


class RFormats:
    """Representation Formats.

    Every format is an alphanumeric key that is used as an object attribute with hasattr(),
    setattr(), and getattr() to store object representations in the corresponding formats.
    """

    # REPRESENTATION FORMAT ENTRIES

    """The USASCII representation format. 

    Implemented as standard pythonic strings, but assured to be USASCII-compatible."""
    USASCII = 'usascii'

    """The UTF-8 representation format. 

    Implemented as standard pythonic strings (as of Python 3.0 and above), encoded in the default UTF-8. """
    UTF8 = 'utf8'

    """The LaTeX representation format.

    Implemented as UTF-8 standard strings with LaTeX encoding.
    """
    LATEX = 'latex'

    """The HTML representation format.

    Implemented as UTF-8 standard strings with HTML character encoding.
    """
    HTML = 'html'

    DOT = 'DOT'
    """DOT Digraph.

    Options should be:
    render DOT source
    render graph as svg, png, etc.

    References:
        * https://graphviz.readthedocs.io/en/stable/manual.html
    """

    # DEFAULT REPRESENTATION FORMAT

    """The default representation format.

    All representations are rendered in the default format, unless specified otherwise."""
    DEFAULT = UTF8  # You may change this.

    # LIST OF REPRESENTATION FORMATS

    """The list of all available formats."""
    CATALOG = [USASCII, UTF8, LATEX, HTML]


# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
# Reference: https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
logging.basicConfig(format='%(message)s')

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
# Reference: https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
logging.root.setLevel(logging.INFO)


def set_debug_level():
    logging.root.setLevel(logging.DEBUG)


def set_info_level():
    logging.root.setLevel(logging.INFO)


def set_warning_level():
    logging.root.setLevel(logging.WARNING)


def set_error_level():
    logging.root.setLevel(logging.ERROR)



COERCION_SUCCESS = 1
COERCION_FAILURE = 2

code_exclusion_list = [1]


def stringify_dictionary(**kwargs):
    s = ''
    for k, v in kwargs.items():
        s = f'{s}\n  {k}: {str(v)}'
    return s
    # return jsonpickle.encode(kwargs)


def log_debug(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'DEBUGGING: {message} {d}.'
        logging.debug(message)


USE_PRINT_FOR_INFO = True
"""Better output in Jupyter notebooks."""


def log_info(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'{message} {d}'
        if USE_PRINT_FOR_INFO:
            print(message)
        else:
            logging.info(message)


class NaiveWarning(UserWarning):
    """The generic category of warning issued by the **naive** library."""
    pass


def log_warning(message: str = '', code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'WARNING: {message} {d}'
        logging.warning(message)


class NaiveError(Exception):
    """The generic exception type raised by the **naive** library."""
    pass


def log_error(message: str = '', *args, code: int = 0, **kwargs):
    if code not in code_exclusion_list:
        d = stringify_dictionary(**kwargs)
        message = f'ERROR: {message}. {d}.'
        logging.error(message, exc_info=True)
        raise NaiveError(message)


def coerce(
        o: (None, object),
        cls: type) -> (None, object):
    """Coerces an object **representation** to type **cls**.

    This function is useful to implement single line argument type coercion for the validation of arguments in functions and methods.

    The assumption behind **coerce** is that all classes implement a coercive constructor.

    Args:
        o (object): An object of undetermined type, but compatible with **cls**.
        cls (type): A class that implements a coercive constructor.

    Returns:
        object: **None**, or an object of type **cls**.

    Raises:
        NaiveWarning: If ambiguous type coercion was necessary.
        NaiveError: If type coercion failed.

    Example:

        .. jupyter-execute::

            # import naive
            n = "5"
            print(n)
            #n_prime = coerce(n, NN0)
            #print(type(n_prime))
            #print(n_prime)

    Notes:
        High-level algorithm:

        1. If **representation** is **None**, returns **None**.

        2. Else if **representation** is of type **cls**, returns **representation**.

        3. Else if **representation** is not of type **cls**, creates an instance of **cls** by calling its default constructor, i.e. ``cls(representation)`` and issue a **NaiveWarning**.


    """
    if o is None:
        return None
    elif isinstance(o, cls):
        # The object is already of the expected type.
        # Return the object itself.
        return o
    else:
        # The object is not of the expected type,
        # we must attempt to force its conversion,
        # by calling the constructor of the desired type,
        # passing it the source object.
        try:
            coerced_o = cls(o)
        except Exception as e:
            log_error(code=COERCION_FAILURE, o=o, cls=cls)
        else:
            log_debug(code=COERCION_SUCCESS, o=o, cls=cls)
        return cls(o)


class ABCRepresentable(abc.ABC):
    """An abstract class for objects that support representation in multiple formats.

    See also:
        * :class:`PersistingRepresentable` class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __str__(self) -> str:
        # TODO: For future development, if images or other media are supported, the output of get_presentation() will need to be converted to text.
        return self.represent()

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        """Less Than.

        Allows sorting of variables by their names.
        Not to be confused with sorting variables by their values."""
        return str(self) < str(other)

    @abc.abstractmethod
    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object's representation in the desired format.

        Args:
            rformat (str): The representation format.
            args:
            kwargs:

        Returns:
            The object's representation in the desired format.
        """
        raise NotImplementedError('Abstract method must be implemented in subclass.')


"""Safe types for type coercion."""
CoercibleABCRepresentable = typing.TypeVar(
    'CoercibleABCRepresentable',
    ABCRepresentable,
    bytes,  # Support for raw USASCII strings.
    str
)


class PersistingRepresentable(ABCRepresentable):
    """A helper class for objects that support representation in multiple formats by storing representations in
    object properties."""

    def __init__(self, source=None, source_representable=None, source_string=None, **kwargs):
        """Initializes the object and stores its representations in available formats.

        Kwargs:
            source_representable (ABCRepresentable): A source source_representable object whose representation should be imitated.
            source_string (source_string): A source object that may be converted to **source_string** to get a UTF-8 representation.
            ...: Representation formats may be passed in kwargs (e.g. usascii='phi', latex=r'\phi').
        """
        if source is not None:
            # Support for implicit conversion during type coercion.
            if isinstance(source, ABCRepresentable):
                source_representable = source
            else:
                source_string = str(source)

        source_representable = coerce(source_representable, ABCRepresentable)
        source_string = coerce(source_string, str)

        self._representations = {}

        if source_representable is not None:
            # If a PersistingRepresentable object was passed as argument,
            # imitate this object's representations.
            self.imitate(source_representable)
        elif source_string is not None:
            # Otherwise, we must assume it was a string or other
            # string-like Unicode representation.
            self._representations[RFormats.UTF8] = source_string

        # If representations are provided in specific formats,
        # store these representations.
        # Note that these get priority over above imitation.
        for arg_key, arg_value in kwargs.items():
            if arg_key in RFormats.CATALOG:
                # This is a representation format.
                if not isinstance(arg_value, str):
                    # TODO: In future development, if images or other media are supported, reconsider this.
                    arg_value = str(arg_value)
                self._representations[arg_key] = arg_value

        super().__init__(**kwargs)

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        """Get the object's representation in a supported format.

        Args:
            rformat (str): A representation format.
            args: For future use.
            kwargs: For future use.

        Returns:
            The object's representation in the requested format.
        """
        if rformat is None:
            rformat = RFormats.DEFAULT
        if rformat in self._representations:
            return self._representations[rformat]
        elif RFormats.UTF8 in self._representations:
            # We fall back on UTF-8
            return self._representations[RFormats.UTF8]
        else:
            raise ValueError(f'PersistingRepresentable object has no representations in {rformat} nor {RFormats.UTF8}.')

    def imitate(self, o: ABCRepresentable):
        """Imitate the representation of another object."""
        for rformat in RFormats.CATALOG:
            # TODO: Minor design flaw: this process will also copy unsupported properties that default to UTF-8.
            self._representations[rformat] = o.represent(rformat)


class Glyph(PersistingRepresentable):
    """A glyph is an elemental representation item."""

    def __init__(self, *args, **kwargs):
        """Initializes a Glyph object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)


class Glyphs:
    # Number sets
    standard_0 = Glyph(utf8='0', latex=r'0', html='0', usascii='0')
    standard_1 = Glyph(utf8='1', latex=r'1', html='1', usascii='1')
    standard_x_lowercase = Glyph(utf8='v', latex=r'v', html='v', usascii='v')
    standard_y_lowercase = Glyph(utf8='y', latex=r'y', html='y', usascii='y')
    standard_z_lowercase = Glyph(utf8='z', latex=r'z', html='z', usascii='z')
    mathbb_a_uppercase = Glyph(utf8='𝔸', latex=r'\mathbb{A}', html='&Aopf;', usascii='A')
    mathbb_b_uppercase = Glyph(utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
    mathbb_n_uppercase = Glyph(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', usascii='N')
    mathbb_z_uppercase = Glyph(utf8='ℤ', latex=r'\mathbb{Z}', html='&Zopf;', usascii='Z')
    # {\displaystyle \mathbb {C} }\mathbb{C} 	ℂ	Complex number	\mathbb{C}, \Complex	&Copf;	U+2102
    # {\displaystyle \mathbb {H} }\mathbb {H} 	ℍ	Quaternion	\mathbb{H}, \H	&quaternions;	U+210D
    # {\displaystyle \mathbb {O} }\mathbb {O} 	𝕆	Octonion	\mathbb{O}	&Oopf;	U+1D546
    # {\displaystyle \mathbb {Q} }\mathbb {Q} 	ℚ	Rational number	\mathbb{Q}, \Q	&Qopf;	U+211A
    # {\displaystyle \mathbb {R} }\mathbb {R} 	ℝ	Real number	\mathbb{R}, \R	&Ropf;	U+211D
    # {\displaystyle \mathbb {S} }\mathbb {S} 	𝕊	Sedenion	\mathbb{S}	&Sopf;	U+1D54A

    to = Glyph(utf8='⟶', latex=r'\longrightarrow', html=r'&rarr;', usascii='-->')
    maps_to = Glyph(utf8='⟼', latex=r'\longmapsto', html=r'&mapsto;', usascii='|->')
    colon = Glyph(utf8=':', latex=r'\colon', html=r':', usascii=':')

    # Bibliography:
    #   * https://en.wikipedia.org/wiki/List_of_logic_symbols
    logical_falsum = Glyph(utf8='⊥', latex=r'\bot', html='&perp;', usascii='F')
    logical_truth = Glyph(utf8='⊤', latex=r'\top', html='&top;', usascii='T')
    logical_negation = Glyph(utf8='¬', latex=r'\lnot', html='&not;', usascii='not')
    logical_conjunction = Glyph(utf8='∧', latex=r'\land', html='&and;', usascii='and')
    logical_disjunction = Glyph(utf8='∨', latex=r'\lor', html='&or;', usascii='or')
    logical_material_implication = Glyph(utf8='⇒', latex=r'\implies', html='&rArr;', usascii='implies')
    logical_material_equivalence = Glyph(utf8='⇔', latex=r'\iif', html='&hArr;', usascii='iif')

    # Greek Letters
    phi_plain_small = Glyph(utf8='φ', latex=r'\phi', html='&phi;', usascii='phi')
    phi_plain_cap = Glyph(utf8='Φ', latex=r'\Phi', html='&Phi;', usascii='Phi')
    psi_plain_small = Glyph(utf8='ψ', latex=r'\psi', html='&psi;', usascii='psi')
    psi_plain_cap = Glyph(utf8='Ψ', latex=r'\Psi', html='&Psi;', usascii='Psi')

    # Brackets
    # Sources:
    #   * https://en.wikipedia.org/wiki/Bracket
    parenthesis_left = Glyph(utf8='(', latex=r'\left(', html='&lparen;', usascii='(')
    parenthesis_right = Glyph(utf8=')', latex=r'\right)', html='&rparen;', usascii=')')
    square_bracket_left = Glyph(utf8='[', latex=r'\left[', html='&91;', usascii='[')
    square_bracket_right = Glyph(utf8=']', latex=r'\right]', html='&93;', usascii=']')
    curly_bracket_left = Glyph(utf8='{', latex=r'\left\{', html='&123;', usascii='{')
    curly_bracket_right = Glyph(utf8='}', latex=r'\right\}', html='&125;', usascii='}')
    angle_bracket_left = Glyph(utf8='⟨', latex=r'\left\langle', html='&lang;', usascii='<')
    angle_bracket_right = Glyph(utf8='⟩', latex=r'\right\rangle', html='&rang;', usascii='>')

    # Set Theory
    element_of = Glyph(utf8='∈∉', latex=r'\in')
    not_element_of = Glyph(utf8='∉', latex=r'\notin')

    # Spaces
    small_space = Glyph(utf8=' ', latex=r'\,', html='&nbsp;', usascii=' ')


"""Safe types for type coercion."""
CoerciblePersistingRepresentable = typing.TypeVar(
    'CoerciblePersistingRepresentable',
    ABCRepresentable,
    bytes,  # Support for raw USASCII strings.
    PersistingRepresentable,
    str
)


def represent(o: object, rformat: str = None, *args, **kwargs) -> str:
    """Get the object'representation representation in the desired format.

    If **representation** is None, return an empty string.
    Else if **representation** is ABCRepresentable, return **representation**.get_representation().
    Else, return source_string(**representation**).

    Args:
        o (object): The object to be represented.
        rformat (str): The representation format.

    Returns:
        The object'representation representation, if support in the desired format.
    """
    if o is None:
        # If nothing is passed for representation,
        # we return an empty string to facilitate concatenations.
        return ''
    if rformat is None:
        rformat = RFormats.DEFAULT
    if isinstance(o, ABCRepresentable):
        return o.represent(rformat, *args, **kwargs)
    else:
        return str(o)


def flatten(*args: object, skip_none: bool = True) -> typing.List[typing.Any]:
    """Flatten iterable objects of arbitrary depth.

    This utility function converts embedded lists or multidimensional objects to vectors.

    If v is already a flat list, returns a new list instance with the same elements.

    If v is not iterable, returns an iterable version of v, that is: [v].

    If v is None, returns an empty list, that is [].

    Args:
        x (object): Any object but preferably an iterable object of type: abc.Iterable[typing.Any].
        skip_none (bool): Do not include None as an element in the resulting list.

    Returns:
         A flat list.

    """
    flattened = []
    for y in args:
        # Recursive call for sub-structures
        # except strings that are understood as atomic in this context
        if isinstance(y, collections.abc.Iterable) and not isinstance(y, str):
            # We cannot call directly extend to support n-depth structures
            sub_flattened = flatten(*y)
            if sub_flattened is not None or not skip_none:
                flattened.extend(sub_flattened)
        elif y is not None or not skip_none:
            flattened.append(y)
    return flattened


def subscriptify(representation: str, rformat: str) -> str:
    """Converts to subscript the representation of object **o**.

    Use cases:
        * Render beautiful indexed math variables (e.g. v₁, v₂, v₃).

    Args:
        representation (str): The representation of the object in that format.
        rformat (str): A supported format from the formats.CATALOG.

    Returns:
        str: The representation in subscript.

    Example:

        .. jupyter-execute::

            # TODO: Rewrite
            #import naive
            #o = 'Indexed math variables look beautiful with subscript: v1, v2, x3'
            #s_prime = subscript(o)
            #print(s_prime)

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    """
    if representation is None:
        return ''
    if rformat is None:
        rformat = RFormats.DEFAULT
    if not isinstance(representation, str):
        representation = str(representation)
    match rformat:
        case RFormats.UTF8:
            # TODO: Extend support to all available subscript characters in Unicode.
            # TODO: Issue a Warning for characters that are not supported and skip them.
            subscript_dictionary = {'0': u'₀',
                                    '1': u'₁',
                                    '2': u'₂',
                                    '3': u'₃',
                                    '4': u'₄',
                                    '5': u'₅',
                                    '6': u'₆',
                                    '7': u'₇',
                                    '8': u'₈',
                                    '9': u'₉'}
            return u''.join(subscript_dictionary.get(char, char) for char in representation)
        case RFormats.LATEX:
            # ASSUMPTION: The subscriptified result must be concatenated with something.
            return r'_{' + representation + r'}'
        case RFormats.HTML:
            return r'<sub>' + representation + r'</sub>'
        case RFormats.USASCII:
            # TODO: USASCII representation may be ambiguous. Considering issuing a Warning.
            return representation


def superscriptify(representation: str, rformat: str = None) -> str:
    """Converts to superscript the representation of object **o**.

    Use cases:
        * Render beautiful indexed math variables (e.g. v₁, v₂, v₃).

    Args:
        representation (str): The representation of the object in that format.
        rformat (str): A supported format from the formats.CATALOG.

    Returns:
        str: The representation in superscript.

    Example:

        .. jupyter-execute::

            # TODO: Rewrite
            #import naive
            #o = 'Indexed math variables look beautiful with superscript: v1, v2, x3'
            #s_prime = superscript(o)
            #print(s_prime)

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    """
    representation = coerce(representation, str)
    if representation is None or representation == '':
        return ''
    if rformat is None:
        rformat = RFormats.DEFAULT
    match rformat:
        case RFormats.UTF8:
            # TODO: Extend support to all available superscript characters in Unicode.
            # TODO: Issue a Warning for characters that are not supported and skip them.
            superscript_dictionary = {'0': u'⁰',
                                      '1': u'¹',
                                      '2': u'²',
                                      '3': u'³',
                                      '4': u'⁴',
                                      '5': u'⁵',
                                      '6': u'⁶',
                                      '7': u'⁷',
                                      '8': u'⁸',
                                      '9': u'⁹'}
            return u''.join(superscript_dictionary.get(char, char) for char in representation)
        case RFormats.LATEX:
            # ASSUMPTION: The superscriptified result must be concatenated with something.
            return r'^{' + representation + r'}'
        case RFormats.HTML:
            return r'<sup>' + representation + r'</sup>'
        case RFormats.USASCII:
            # TODO: USASCII representation may be ambiguous. Considering issuing a Warning.
            return representation


def unkwargs(kwargs, key):
    return None if key not in kwargs else kwargs[key]


def extract_scope_key_from_qualified_key(qualified_key):
    """Extract the scope_key key from a qualified key."""
    if qualified_key is None:
        return None
    else:
        qualified_key = str(qualified_key)
        first_separator_position = qualified_key.find(_QUALIFIED_KEY_SEPARATOR)
        return qualified_key[0, first_separator_position]


def clean_mnemonic_key(mnemonic_key):
    if mnemonic_key is None:
        log_error('NKey is None')
    else:
        mnemonic_key = str(mnemonic_key)
        return ''.join(c for c in mnemonic_key if c in _MNEMONIC_KEY_ALLOWED_CHARACTERS)


def set_default_scope(scope_key):
    """Sets the default user-defined scope. Creates it if necessary.

    Args:
        scope_key (str): A unique key to identify the user-defined scope.

    Returns:
        N/A

    Example:

        .. jupyter-execute::
            :raises:
            :stderr:

            initial_scope = naive.get_default_scope()
            print(f'The initial scope was: "{initial_scope}"')

            naive.set_default_scope('my_scope')
            print('Do something...\n')

            naive.set_default_scope('another_scope')
            print('Do something else...\n')
            
            naive.set_default_scope(initial_scope)
            print('Do yet something else...\n')

    """
    global _DEFAULT_SCOPE_KEY
    # TODO: Allow the usage of friendly name, notes or documentation, etc.
    if scope_key is None:
        log_error(
            f'None is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    if not isinstance(scope_key, str):
        log_error(
            f'The object "{scope_key}" of type "{type(scope_key)}" is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    scope_key_cleaned = clean_mnemonic_key(scope_key)
    if scope_key_cleaned != scope_key:
        log_warning(
            f'Please note that the context key "{scope_key}" contained unsupported characters. The allowed characters for context keys are: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}". It was automatically cleaned from unsupported characters. The resulting context key is: {scope_key_cleaned}')
    if scope_key == '':
        log_error(
            f'An empty string is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')

    prefixed_key = Core._USER_DEFINED_KEY_PREFIX + scope_key_cleaned
    _DEFAULT_SCOPE_KEY = prefixed_key
    log_info(f'Default scope_key: {scope_key_cleaned}')


def get_default_scope():
    return _DEFAULT_SCOPE_KEY[len(Core._USER_DEFINED_KEY_PREFIX):]




def av(codomain, base_name=None, indexes=None):
    """Shorthand alias for :ref:`declare_atomic_variable` **declare_atomic_variable**."""
    return Core.declare_atomic_variable(codomain, base_name, indexes)



class Counter(object):
    def __init__(self):
        self.value = 1
        self._lock = threading.Lock()

    def get_value(self):
        with self._lock:
            self.value += 1
            return self.value




def f(o, *args):
    """Shorthand function to write a formula."""
    return Core.write_formula(o, *args)



def get_qualified_key(scope_key, structure_key, language_key, base_key):
    return f'{scope_key}{_QUALIFIED_KEY_SEPARATOR}{structure_key}{_QUALIFIED_KEY_SEPARATOR}{language_key}{_QUALIFIED_KEY_SEPARATOR}{base_key}'



_QUALIFIED_KEY_SEPARATOR = '.'
_MNEMONIC_KEY_ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz012345679_'

_concept_database = {}
"""The static database of concepts."""

_token_database = {}
"""The static database of tokens."""

class Core:
    _BASE_KEY = 'base_key'
    _STRUCTURE_KEY = 'structure_key'
    _SCOPE_KEY = 'scope_key'
    _LANGUAGE_KEY = 'language_key'

    # SystemFunction Complementary Properties
    _DOMAIN = 'codomain'
    _CODOMAIN = 'codomain'
    _ARITY = 'arity'
    _PYTHON_VALUE = 'python_value'

    # NType Keys
    _STRUCTURE_SCOPE = 'scope_key'
    _STRUCTURE_LANGUAGE = 'language_key'
    _STRUCTURE_DOMAIN = 'codomain'
    _STRUCTURE_FUNCTION = 'function'
    _STRUCTURE_ATOMIC_PROPERTY = 'ap'
    _STRUCTURE_VARIABLE = 'variable'
    _STRUCTURE_FORMULA = 'formula'

    _DEFAULT_SCOPE_KEY = ''
    _SYSTEM_DEFINED_KEY_PREFIX = 'sys_'
    _USER_DEFINED_KEY_PREFIX = 'ud_'
    _LANGUAGE_NAIVE = 'naive'



    class Concept:

        global _concept_database
        global _token_database

        def __init__(self, scope_key, structure_key, language_key, base_key,
                     utf8=None, latex=None, html=None, usascii=None, tokens=None,
                     domain=None, codomain=None, arity=None, pythong_value=None,
                     **kwargs):
            # Identification Properties that constitute the Qualified Key.
            if scope_key is None:
                scope_key = get_default_scope()
            self._scope_key = clean_mnemonic_key(scope_key)
            self._structure_key = clean_mnemonic_key(structure_key)
            self._language_key = clean_mnemonic_key(language_key)
            self._base_key = clean_mnemonic_key(base_key)
            # Representation Properties
            self._utf8 = utf8
            self._latex = latex
            self._html = html
            self._usascii = usascii
            self._tokens = tokens
            # Populate the token-concept mapping
            # to facilitate the retrieval of concepts during parsing
            # TODO: Consider the following approach: append utf8, latex, etc. as primary tokens,
            #  and consider the tokens argument for complementary tokens only.
            if self.tokens is not None:
                for token in self.tokens:
                    if token not in _token_database:
                        # TODO: Question: should we store a reference to the Concept or store the Concept qualified key?
                        _token_database[token] = self
                    else:
                        log_error(
                            f'The "{token}" token was already in the token static database. We need to implement a priority algorithm to manage these situations.',
                            token=token, self=self)
            # Append the concept in the database
            if self.qualified_key not in _concept_database:
                _concept_database[self.qualified_key] = self
            else:
                log_error(
                    'The initialization of the concept could not be completed because the qualified key was already present in the static database.',
                    qualified_key=self.qualified_key)

        def __str__(self):
            return self.represent(RFormats.UTF8)

        def __repr__(self):
            return self.represent(RFormats.UTF8)

        @property
        def arity(self):
            return self._arity

        @property
        def base_key(self):
            return self._base_key

        @staticmethod
        def check_concept_from_decomposed_key(scope_key: str, structure_key: str, language_key: str, base_key: str,
                                              **kwargs):
            if scope_key is not None and structure_key is not None and language_key is not None and base_key is not None:
                qualified_key = get_qualified_key(scope_key, structure_key, language_key, base_key)
                return Core.Concept.check_concept_from_qualified_key(
                    qualified_key, scope=scope_key, ntype=structure_key, language=language_key, nkey=base_key,
                    **kwargs)
            else:
                log_error('Some identification properties are None', scope=scope_key, ntype=structure_key,
                          language=language_key, nkey=base_key, **kwargs)

        @staticmethod
        def check_concept_from_qualified_key(qualified_key, **kwargs):
            if qualified_key is not None:
                return qualified_key in _concept_database
            else:
                log_error('Checking concept with None qualified key is impossible.',
                          qualified_key=qualified_key, **kwargs)

        @staticmethod
        def get_concept_from_decomposed_key(scope_key: str, structure_key: str, language_key: str, base_key: str,
                                            **kwargs):
            if scope_key is not None and structure_key is not None and language_key is not None and base_key is not None:
                qualified_key = get_qualified_key(scope_key, structure_key, language_key, base_key)
                return Core.Concept.get_concept_from_qualified_key(
                    qualified_key, scope=scope_key, ntype=structure_key, language=language_key, nkey=base_key,
                    **kwargs)
            else:
                log_error('Some identification properties are None', scope=scope_key, ntype=structure_key,
                          language=language_key, nkey=base_key, **kwargs)

        @staticmethod
        def get_concept_from_qualified_key(qualified_key, **kwargs):
            if qualified_key is not None:
                if qualified_key in _concept_database:
                    return _concept_database[qualified_key]
                else:
                    return Core.Concept(qualified_key=qualified_key, **kwargs)
            else:
                log_error('Getting concept with None qualified key is impossible.',
                          qualified_key=qualified_key, **kwargs)

        @staticmethod
        def get_concept_from_token(token):
            """

            Definition:
            A **token** is a list of text symbols that is mapped to a specific concept.
            """
            # TODO: Resume implementation here.
            #   - In Concept __init__: subscribe tokens to a global indexes and check for unicity.
            if token in Core.Concept._token_database:
                return Core.Concept._token_database[token]
            else:
                return None

        def is_equal_concept(self, other: Core.Concept):
            return self.qualified_key == other.qualified_key

        @property
        def language(self):
            return self._language_key

        def represent(self, rformat: str = None, *args, **kwargs) -> str:
            """Get the object's representation in a supported format.

            Args:
                rformat (str): A representation format.
                args: For future use.
                kwargs: For future use.

            Returns:
                The object's representation in the requested format.
            """
            if rformat is None:
                rformat = RFormats.DEFAULT
            # TODO: Check that rformat is an allowed value.
            if hasattr(self, rformat):
                return getattr(self, rformat)
            elif self._utf8 is not None:
                # We fall back on UTF-8
                return self._utf8
            else:
                log_error(f'This concept has no representation in {rformat} nor {RFormats.UTF8}.', rformat=rformat,
                          qualified_key=self.qualified_key)

        @property
        def structure_key(self) -> str:
            return self._structure_key

        @property
        def python_value(self):
            return self._python_value

        @property
        def qualified_key(self):
            return get_qualified_key(scope_key=self.scope_key, structure_key=self.structure_key,
                                     language_key=self.language,
                                     base_key=self.base_key)

        @property
        def scope_key(self):
            return self._scope_key

        @property
        def tokens(self):
            return self._tokens

    class Language(Concept):
        def __init__(
                self,
                # Identification properties
                scope_key, structure_key, language_key, base_key,
                # Mandatory complementary properties
                # Conditional complementary properties
                # Representation properties
                utf8=None, latex=None, html=None, usascii=None, tokens=None,
                **kwargs):
            # ...

            # Call the base class initializer.
            #   Executing this at the end of the initialization process
            #   assures that the new concept is not appended to the
            #   static concept and token databases before it is fully initialized.
            super().__init__(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
                **kwargs)

    class Domain(Concept):
        def __init__(
                self,
                # Identification properties
                scope_key, structure_key, language_key, base_key,
                # Mandatory complementary properties
                # Conditional complementary properties
                # Representation properties
                utf8=None, latex=None, html=None, usascii=None, tokens=None,
                **kwargs):
            # ...

            # Call the base class initializer.
            #   Executing this at the end of the initialization process
            #   assures that the new concept is not appended to the
            #   static concept and token databases before it is fully initialized.
            super().__init__(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
                **kwargs)

    class Scope(Concept):
        def __init__(
                self,
                # Identification properties
                scope_key, structure_key, language_key, base_key,
                # Mandatory complementary properties
                # Conditional complementary properties
                # Representation properties
                utf8=None, latex=None, html=None, usascii=None, tokens=None,
                **kwargs):
            # Call the base class initializer.
            #   Executing this at the end of the initialization process
            #   assures that the new concept is not appended to the
            #   static concept and token databases before it is fully initialized.
            super().__init__(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
                **kwargs)

    # Scope.
    system_scope = Scope(
        scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE, base_key='sys',
        utf8='sys', latex=r'\text{sys}', html='sys', usascii='sys')

    initial_user_defined_scope = Scope(
        scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE,
        base_key=_USER_DEFINED_KEY_PREFIX + 'scope_1',
        utf8='scope_key₁', latex=r'\text{scope_key}_1', html=r'scope_key<sub>1</sub>', usascii='scope1')


    class SystemFunction(Concept):
        """The system function class.

        Definition:
        A system function, in the context of the naive package,
        is a function that is predefined in the sense that it is accompanied by a programmatic algorithm and not a formula,
        and atomic in the sense that it cannot be further decomposed into constituent sub-formulae.

        """

        # Constants
        SYSTEM_CONSTANT = 'atomic_constant'  # Aka a 0-ary function.
        SYSTEM_UNARY_OPERATOR = 'atomic_unary_operator'  # Aka a unary function with operator notation.
        SYSTEM_BINARY_OPERATOR = 'atomic_binary_operator'  # Aka a binary function with operator notation.
        SYSTEM_N_ARY_FUNCTION = 'atomic_n_ary_function'
        CATEGORIES = [SYSTEM_CONSTANT, SYSTEM_UNARY_OPERATOR, SYSTEM_BINARY_OPERATOR, SYSTEM_N_ARY_FUNCTION]

        def __init__(
                self,
                # Identification properties
                scope_key, structure_key, language_key, base_key,
                # Mandatory complementary properties
                category, codomain, algorithm,
                # Conditional complementary properties
                domain=None, arity=None, python_value=None,
                # Representation properties
                utf8=None, latex=None, html=None, usascii=None, tokens=None,
                **kwargs):
            # Mandatory complementary properties.
            self._codomain = codomain  # TODO: Implement validation against the static concept database.
            self._algorithm = algorithm
            if category not in Core.SystemFunction.CATEGORIES:
                log_error('Invalid formula category',
                          category=category, qualified_key=self.qualified_key)
            self._category = category
            # Conditional complementary properties.
            self._domain = domain  # TODO: Implement validation against the static concept database.
            self._arity = arity  # TODO: Implement validation logic dependent of subcategory.
            if category == Core.SystemFunction.SYSTEM_CONSTANT and python_value is None:
                log_error('python_value is mandatory for constants (0-ary functions) but it was None.',
                          python_value=python_value, category=category, qualified_key=self.qualified_key)
            self._python_value = python_value  # TODO: Question: Should it be mandatory for subcategory = constant?
            # Call the base class initializer.
            #   Executing this at the end of the initialization process
            #   assures that the new concept is not appended to the
            #   static concept and token databases before it is fully initialized.
            super().__init__(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
                **kwargs)

        @property
        def algorithm(self):
            return self._algorithm

        @property
        def category(self):
            return self._category

        @property
        def codomain(self):
            return self._codomain

        @property
        def domain(self):
            return self._domain

        @property
        def compute_programmatic_value(self):
            # TODO: The idea is to distinguish the computerized or programmatic value,
            #   here as a canonical mapping to a python object,
            #   with the symbolic value, the later being the naive concept.
            if self.category == Core.SystemFunction.SYSTEM_CONSTANT:
                return self._python_value
            else:
                raise NotImplementedError('ooops')

        def equal_programmatic_value(self, other):
            """Return true if two formula yield identical values, false otherwise."""
            if isinstance(other,
                          Core.Formula) and other.subcategory == Core.SystemFunction.SYSTEM_CONSTANT:  # Using a union type to avoid import issues.
                return self.compute_programmatic_value() == other.compute_programmatic_value()
            else:
                raise NotImplementedError('oooops again')


    class Formula(Concept):
        """

        Definition:
        A formula, in the context of the naive package,
        is a tree of "calls" to functions, constants, or variables.
        ...

        Different types of formula:
        - Atomic Variable (aka Unknown) (e.g. x + 5 = 17, x ∉ ℕ₀)
        - Formula Variable (e.g. φ = ¬x ∨ y, z ∧ φ)
        - n-ary SystemFunction Call with n in N0 (e.g. za1 abs)

        Different sub-types of n-ary Functions:
        - 0-ary Operator (aka Constant) (e.g. ba1_language truth)
        - Unary Operator (e.g. ba1_language negation)
        - Binary Operator (e.g. ba1_language conjunction)
        - n-ary SystemFunction

        """
        # TODO: Issue a warning when a property is accessed when the category make it invalid.

        # Constants
        ATOMIC_VARIABLE = 'formula_atomic_variable'  # TODO: Question: is it justified to distinguish this from FORMULA_VARIABLE?
        FORMULA_VARIABLE = 'formula_formula_variable'  # TODO: Question: is it justified to distinguish this from ATOMIC_VARIABLE?
        SYSTEM_CONSTANT_CALL = 'formula_constant_call'  # Aka a 0-ary function.
        SYSTEM_UNARY_OPERATOR_CALL = 'formula_unary_operator_call'
        SYSTEM_BINARY_OPERATOR_CALL = 'formula_binary_operator_call'
        SYSTEM_N_ARY_FUNCTION_CALL = 'formula_n_ary_function_call'
        CATEGORIES = [ATOMIC_VARIABLE, FORMULA_VARIABLE, SYSTEM_CONSTANT_CALL, SYSTEM_UNARY_OPERATOR_CALL,
                      SYSTEM_BINARY_OPERATOR_CALL,
                      SYSTEM_N_ARY_FUNCTION_CALL]

        def __init__(
                self,
                # Identification properties
                scope_key, language_key, base_key,
                # Mandatory complementary properties
                category,
                # Conditional complementary properties
                # ...for system function calls:
                system_function=None, arguments=None,
                # ...for atomic variables
                domain=None, codomain=None, base_name=None, indexes=None,
                **kwargs):
            # Identification properties
            structure_key = Core._STRUCTURE_FORMULA
            # Mandatory complementary properties.
            if category not in Core.Formula.CATEGORIES:
                log_error('Invalid formula category',
                          category=category,
                          scope_key=scope_key, language_key=language_key, base_key=base_key,
                          system_function=system_function, arguments=arguments,
                          domain=domain, codomain=codomain, base_name=base_name, indexes=indexes)
            self._category = category
            self._arity = None
            self._system_function = system_function
            # match category:
            #     case Formula.ATOMIC_VARIABLE:
            #         # The rationale for this arity = 0 is that atomic variables have no input.
            #         # This would be wrong of formula variables.
            #         self._arity = 0
            #     case Formula.SYSTEM_CONSTANT_CALL:
            #         self._arity = 0
            #     case Formula.SYSTEM_UNARY_OPERATOR_CALL:
            #         self._arity = 1
            #     case Formula.SYSTEM_BINARY_OPERATOR_CALL:
            #         self._arity = 2
            #     # Replace the match ... case ... with system.function.arity.
            #     # TODO: Implement arity for n-ary system function calls.
            #     # TODO: Implement arity for formula variables.
            #     # TODO: Consider making this property a dynamic property.
            self._arguments = arguments
            self._domain = 'NOT IMPLEMENTED'  # TODO: Implement formula domain. It may be None, a base domain or a tuple of domains.
            self._codomain = codomain  # TODO: Check that codomain is only passed as argument when appicable. Otherwise, issue a warning.
            self._base_name = base_name
            self._indexes = indexes
            # Call the base class initializer.
            #   Executing this at the end of the initialization process
            #   assures that the new concept is not appended to the
            #   static concept and token databases before it is fully initialized.
            super().__init__(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                **kwargs)

        @property
        def arguments(self):
            return self._arguments

        @property
        def arity(self):
            if self.category == Core.Formula.ATOMIC_VARIABLE:
                # For atomic variables, the arity is 0.
                # The rationale is that an atomic variable doesn't get any input.
                # This would be wrong of formula variables which deserver a distinct implementation.
                return 0
            elif self.is_system_function_call:
                # For system function calls, the arity of the call
                # is equal to the arity of the function being called.
                return self.system_function.arity
            else:
                # TODO: Implement the arity property for all object categories.
                log_warning('The arity property has not been implemented for this concept category.',
                            category=self.category, self=self)

        @property
        def category(self):
            return self._category

        @property
        def codomain(self):
            if self.category == Core.Formula.ATOMIC_VARIABLE:
                # For atomic variables, the codomain is part of the object.
                return self._codomain
            elif self.is_system_function_call:
                # For system function calls, the codomain of the function call
                # is equal to the codomain of the function being called.
                return self.system_function.codomain
            else:
                # TODO: Implement the codomain property for all object categories.
                log_warning('The codomain property has not been implemented for this concept category.',
                            category=self.category, self=self)

        @property
        def domain(self):
            raise NotImplementedError('Please implement the domain property')
            return self._domain

        @property
        def indexes(self):
            return self._indexes

        @property
        def is_system_function_call(self):
            """Return *True* if this is a system function call, *False* otherwise.

            If *True*, the instance has the *system_function* property.
            """
            return self.category in [
                Core.Formula.SYSTEM_CONSTANT_CALL,
                Core.Formula.SYSTEM_UNARY_OPERATOR_CALL,
                Core.Formula.SYSTEM_BINARY_OPERATOR_CALL,
                Core.Formula.SYSTEM_N_ARY_FUNCTION_CALL]

        def list_atomic_variables(self):
            """Return the sorted set of variables present in the formula, and its subformulae recursively."""
            l = set()
            for a in self.arguments:
                if isinstance(a,
                              Core.Formula) and a.category == Core.Formula.ATOMIC_VARIABLE:  # Using a union type to avoid import issues.
                    l.add(a)
                elif isinstance(a, Core.Formula):  # Using a union type to avoid import issues.
                    l_prime = a.list_atomic_variables()
                    for a_prime in l_prime:
                        l.add(a_prime)
                else:
                    log_error('Not implemented yet', a=a, self=self)

            # To allow sorting and indexing, convert the set to a list.
            l = list(l)
            l.sort(key=lambda x: x.base_key)
            return l

        def represent(self, rformat: str = None, *args, **kwargs) -> str:
            if rformat is None:
                rformat = RFormats.DEFAULT
            # if self.category == Formula.ATOMIC_VARIABLE:
            #     return self.symbol.represent(rformat, *args, **kwargs)
            match self.category:
                case Core.Formula.ATOMIC_VARIABLE:
                    # x
                    # TODO: Modify approach. Storing and returning the _base_name like this
                    #   prevent support for other mathematical fonts, such as MathCal, etc.
                    #   As an initial approach, it provides support for ASCII like variables.
                    #   We may consider storing a Glyph as the base name,
                    #   and calling the static represent() function.
                    return self._base_name + \
                           subscriptify(represent(self._indexes, rformat), rformat)
                case Core.Formula.SYSTEM_CONSTANT_CALL:
                    # x
                    return f'{self._system_function.represent(rformat)}'
                case Core.Formula.SYSTEM_UNARY_OPERATOR_CALL:
                    # fx
                    return f'{self._system_function.represent(rformat)}{self.arguments[0].represent(rformat)}'
                case Core.Formula.SYSTEM_BINARY_OPERATOR_CALL:
                    # (x f y)
                    return f'{Glyphs.parenthesis_left.represent(rformat)}{self.arguments[0].represent(rformat)}{Glyphs.small_space.represent(rformat)}{self._system_function.represent(rformat)}{Glyphs.small_space.represent(rformat)}{self.arguments[1].represent(rformat)}{Glyphs.parenthesis_right.represent(rformat)}'
                case Core.Formula.SYSTEM_N_ARY_FUNCTION_CALL:
                    # f(x,y,z)
                    variable_list = ', '.join(map(lambda a: a.represent(), self.arguments))
                    return f'{self._system_function.represent(rformat)}{Glyphs.parenthesis_left.represent(rformat)}{variable_list}{Glyphs.parenthesis_right.represent(rformat)}'
                case _:
                    log_error('Unsupported formula category', category=self.category, qualified_key=self.qualified_key)

        def represent_declaration(self, rformat: str = None, *args, **kwargs) -> str:
            if self.category != Core.Formula.ATOMIC_VARIABLE:
                log_error('Formula category not supported for declaration.')
            else:
                if rformat is None:
                    rformat = RFormats.DEFAULT
                match rformat:
                    case RFormats.UTF8:
                        return f'With {self.represent(rformat)} ∈ {self.codomain.represent(rformat)}.'
                    case _:
                        raise NotImplementedError('TODO')

        @property
        def system_function(self):
            return self._system_function

    _FORMULA_AUTO_COUNTER = Counter()

    @staticmethod
    def write_formula(o, *args):
        global _FORMULA_AUTO_COUNTER
        scope_key = _DEFAULT_SCOPE_KEY
        index = Core._FORMULA_AUTO_COUNTER.get_value()
        base_key = 'f' + str(index)
        category = None
        system_function = None
        if isinstance(o, Core.SystemFunction):  # Using a union type to avoid import issues.
            system_function = o
            match o.category:
                case Core.SystemFunction.SYSTEM_CONSTANT:
                    category = Core.Formula.SYSTEM_CONSTANT_CALL
                case Core.SystemFunction.SYSTEM_UNARY_OPERATOR:
                    category = Core.Formula.SYSTEM_UNARY_OPERATOR_CALL
                case Core.SystemFunction.SYSTEM_BINARY_OPERATOR:
                    category = Core.Formula.SYSTEM_BINARY_OPERATOR_CALL
                # TODO: Implement all other possibilities
        arguments = args
        formula = Core.Formula(
            # Identification properties
            scope_key=scope_key, language_key=Core._LANGUAGE_NAIVE, base_key=base_key,
            # Mandatory complementary properties
            category=category,
            # Conditional complementary properties
            system_function=system_function, arguments=arguments
        )
        log_info(formula.represent())
        return formula

    @staticmethod
    def declare_atomic_variable(codomain, base_name=None, indexes=None):
        # TODO: Provide support for different math fonts (e.g.: https://www.overleaf.com/learn/latex/Mathematical_fonts)
        # TODO: Provide support for indexed variables. Variable declaration should be made with indexes bounds and not individual indexes values.
        codomain_key = None
        # Identification properties
        scope_key = _DEFAULT_SCOPE_KEY
        structure_key = Core._STRUCTURE_FORMULA
        language_key = Core._LANGUAGE_NAIVE
        if base_name is None:
            # TODO: Make this a scope preference setting, letting the user choose the default
            #   variable base_name in that scope.
            base_name = 'x'
        base_key = base_name
        if indexes is not None:
            if not isinstance(indexes, collections.abc.Iterable):
                base_key = base_key + '__' + str(indexes)
            else:
                base_key = base_key + '__' + '_'.join(str(index) for index in indexes)
        if Core.Concept.check_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key,
                                                     language_key=language_key, base_key=base_key):
            variable = Core.Concept.get_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key,
                                                               language_key=language_key, base_key=base_key)
            log_warning(
                'This variable is already declared. In consequence, the existing variable is returned, instead of declaring a new one.',
                variable=variable, scope_key=scope_key)
            return variable
        else:
            variable = Core.Formula(
                scope_key=scope_key, language_key=language_key, base_key=base_key,
                category=Core.Formula.ATOMIC_VARIABLE,
                codomain=codomain, base_name=base_name, indexes=indexes)
            log_info(variable.represent_declaration())
            return variable


# TODO: Question: what should be the scope_key of user defined scopes? sys? the scope_key itself?

def convert_formula_to_graphviz_digraph(formula: Core.Formula, digraph=None):
    title = formula.represent(RFormats.UTF8)
    id = formula.qualified_key

    if digraph is None:
        digraph = graphviz.Digraph(id)

    digraph.node(id, title)
    if isinstance(formula, Core.Formula) and isinstance(formula.arguments, collections.abc.Iterable):
        for argument in formula.arguments:
            convert_formula_to_graphviz_digraph(formula=argument, digraph=digraph)
            digraph.edge(id, argument.qualified_key, dir='back')

    return digraph


def convert_formula_to_dot(formula: Core.Formula):
    digraph = convert_formula_to_graphviz_digraph(formula=formula)
    return digraph.source


def render_formula_as_ipython_mimebundle(formula: Core.Formula):
    """
    Render the formula as a digraph in SVG format,
    in Jupyter Notebook, Jupyter QT Console, and/or insider Spyder IDE.

    Bibliography:
        * https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Graph._repr_mimebundle_
        * https://graphviz.readthedocs.io/en/stable/manual.html
    """
    digraph = convert_formula_to_graphviz_digraph(formula=formula)
    digraph._repr_mimebundle_()



class BA1:
    _SCOPE_BA1 = 'sys_ba1'
    _LANGUAGE_BA1 = 'ba1_language'


    # Dirty little trick to overcome circular references
    # between algorithm function definitions,
    # and system function definitions.
    # These global variables are overwritten at the end
    # of this module.
    truth = None
    falsum = None


    # Scope.
    ba1_scope = Core.Scope(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_SCOPE, language_key=_LANGUAGE_BA1, base_key='ba1_language',
        utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

    # Language.
    ba1_language = Core.Language(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_LANGUAGE, language_key=_LANGUAGE_BA1,
        base_key='ba1_language',
        utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

    # Domains.
    b = Core.Domain(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b',
        utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
    b2 = Core.Domain(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b2',
        utf8='𝔹²', latex=r'\mathbb{B}^{2}', html=r'&Bopf;<sup>2</sup>', usascii='B2')


    # Algorithms.
    @staticmethod
    def falsum_algorithm(vector_size: int = 1) -> typing.List[Core.SystemFunction]:
        """The vectorized falsum boolean function.

        Returns:
            BooleanConstant: The boolean falsum.
        """
        return [BA1.falsum] * vector_size

    @staticmethod
    def truth_algorithm(vector_size: int = 1) -> typing.List[Core.SystemFunction]:
        """The vectorized truth boolean function.

        Returns:
            BooleanConstant: The boolean truth.
        """
        return [BA1.truth] * vector_size

    @staticmethod
    def negation_algorithm(v: typing.List[Core.SystemFunction]) -> typing.List[Core.SystemFunction]:
        """The vectorized negation boolean function.

        Args:
            v (typing.List[BooleanConstant]): A vector of boolean constants.

        Returns:
            typing.List[BooleanConstant]: A vector of the negation of **x**.
        """
        # v = coerce(v, BooleanConstant)  # TODO: Consider support for list coercion.
        v = flatten(v)  # If scalar, convert to list.
        return [BA1.falsum if e == BA1.truth else BA1.truth for e in v]

    @staticmethod
    def conjunction_algorithm(
            v1: typing.List[Core.SystemFunction],
            v2: typing.List[Core.SystemFunction]) -> \
            typing.List[Core.SystemFunction]:
        """The vectorized conjunction boolean function.

        Args:
            v1 (typing.List[BooleanConstant]): A vector of boolean constants.
            v2 (typing.List[BooleanConstant]): A vector of boolean constants.

        Returns:
            typing.List[BooleanConstant]: The vector of the conjunction of **v1** and **v2**.
        """
        # v1 = coerce(v1, BooleanConstant)  # TODO: Consider support for list coercion.
        # v2 = coerce(v2, BooleanConstant)  # TODO: Consider support for list coercion.
        v1 = flatten(v1)  # If scalar, convert to list.
        v2 = flatten(v2)  # If scalar, convert to list.
        return [BA1.truth if (b1 == BA1.truth and b2 == BA1.truth) else BA1.falsum for b1, b2 in zip(v1, v2)]

    @staticmethod
    def disjunction_algorithm(
            v1: typing.List[Core.SystemFunction],
            v2: typing.List[Core.SystemFunction]) -> \
            typing.List[Core.SystemFunction]:
        """The vectorized disjunction boolean function.

        Args:
            v1 (typing.List[BooleanConstant]): A vector of boolean constants.
            v2 (typing.List[BooleanConstant]): A vector of boolean constants.

        Returns:
            typing.List[BooleanConstant]: The vector of the disjunction of **v1** and **v2**.
        """
        # v1 = coerce(v1, BooleanConstant)  # TODO: Consider support for list coercion.
        # v2 = coerce(v2, BooleanConstant)  # TODO: Consider support for list coercion.
        v1 = flatten(v1)  # If scalar, convert to list.
        v2 = flatten(v2)  # If scalar, convert to list.
        return [BA1.truth if (b1 == BA1.truth or b2 == BA1.truth) else BA1.falsum for b1, b2 in zip(v1, v2)]


    # Functions.
    truth = Core.SystemFunction(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='truth',
        codomain=b, category=Core.SystemFunction.SYSTEM_CONSTANT, algorithm=truth_algorithm,
        utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
        arity=0, python_value=True)

    falsum = Core.SystemFunction(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='falsum',
        codomain=b, category=Core.SystemFunction.SYSTEM_CONSTANT, algorithm=falsum_algorithm,
        utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
        arity=0, python_value=False)
    negation = Core.SystemFunction(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='negation',
        codomain=b, category=Core.SystemFunction.SYSTEM_UNARY_OPERATOR, algorithm=negation_algorithm,
        utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
        domain=b, arity=1)
    conjunction = Core.SystemFunction(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1,
        base_key='conjunction',
        codomain=b, category=Core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=conjunction_algorithm,
        utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
        domain=b, arity=2)
    disjunction = Core.SystemFunction(
        scope_key=_SCOPE_BA1, structure_key=Core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1,
        base_key='disjunction',
        codomain=b, category=Core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=disjunction_algorithm,
        utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
        domain=b, arity=2)

    @staticmethod
    def get_bn_domain(n):
        """Returns the n-tuple codomain 𝔹ⁿ where n is a natural number > 0.

        Assures the presence of the codomain 𝔹ⁿ in the concept database.
        """
        if not isinstance(n, int):
            log_error('n must be an int')
        elif n < 1:
            log_error('n must be > 1')
        elif n == 1:
            return BA1.b
        elif n == 2:
            return BA1.b2
        else:
            scope_key = BA1._SCOPE_BA1
            structure_key = Core._STRUCTURE_DOMAIN
            language_key = BA1._LANGUAGE_BA1
            base_key = 'b' + str(n)  # TODO: Check it is an int
            # TODO: Consider implementing a lock to avoid bugs with multithreading when checking the static dictionary
            if Core.Concept.check_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key,
                                                         language_key=language_key, base_key=base_key):
                return Core.Concept.get_concept_from_decomposed_key(scope_key=scope_key,
                                                               structure_key=structure_key,
                                                               language_key=language_key, base_key=base_key)
            else:
                return Core.Domain(
                    scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                    utf8='𝔹' + superscriptify(n), latex=r'\mathbb{B}^{' + str(n) + r'}',
                    html=r'&Bopf;<sup>' + str(n) + '</sup>', usascii='B' + str(n))

    @staticmethod
    def get_boolean_combinations_column(n, c):
        """
        Bibliography:
            * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
        """
        # TODO: Assure endianness consistency.
        return [(BA1.truth if (integer_value & 1 << c != 0) else BA1.falsum) for integer_value in range(0, 2 ** n)]

    @staticmethod
    def satisfaction_index(phi: Core.Formula, variables_list=None):
        """Compute the **satisfaction indexes** (:math:`\text{sat}_I`) of a Boolean formula (:math:`\phi`).

        Alias:
        **sat_i**

        Definition:
        Let :math:`\phi` be a Boolean formula.
        :math:`\text{sat}_I \colon= ` the truth value of :math:`\phi` in all possible worlds.

        Args:
            phi (BooleanFormula): The Boolean formula :math:`\phi` .
        """
        # Retrieve the computed results
        # TODO: Check that all formula are Boolean formula. Otherwise, the formula
        #   may not return a Boolean value, forbidding the computation of a satisfaction set.
        if variables_list is None:
            variables_list = phi.list_atomic_variables()
        variables_number = len(variables_list)
        arguments_number = phi.arity
        argument_vectors = [None] * arguments_number
        log_debug(arguments_number=arguments_number)
        for argument_index in range(0, arguments_number):
            argument = phi.arguments[argument_index]
            log_debug(
                argument=argument,
                argument_index=argument_index,
                argument_type=type(argument),
                argument_codomain=argument.codomain,
                argument_is_system_function_call=argument.is_system_function_call)
            if isinstance(argument, Core.Formula) and \
                    argument.is_system_function_call and \
                    argument.codomain == BA1.b:
                # This argument is a Boolean Formula.
                log_debug('This argument is a Boolean Formula')
                # Recursively compute the satisfaction set of that formula,
                # restricting the variables list to the subset of necessary variables.
                vector = BA1.satisfaction_index(argument, variables_list=variables_list)
                argument_vectors[argument_index] = vector
            elif isinstance(argument, Core.Formula) and \
                    argument.category == Core.Formula.ATOMIC_VARIABLE and \
                    argument.codomain == BA1.b:
                # This argument is a Boolean atomic proposition.
                log_debug('This argument is a Boolean atomic proposition')
                # We want to retrieve its values from the corresponding bit combinations column.
                # But we need the vector to be relative to variables_list.
                # Thus we must first find the position of this atomic variable,
                # in the variables_list.
                atomic_variable_index = variables_list.index(argument)
                vector = BA1.get_boolean_combinations_column(variables_number, atomic_variable_index)
                log_debug(vector=vector)
                argument_vectors[argument_index] = vector
            else:
                log_error('Unexpected type', argument=argument, t=type(argument), category=argument.category,
                          codomain=argument.codomain)
        log_debug(argument_vectors=argument_vectors)
        output_vector = None
        log_debug(phi=phi, arity=phi.arity, system_function=phi.system_function)
        match phi.arity:
            case 0:
                output_vector = phi.system_function.algorithm(vector_size=2 ** variables_number)
            case 1:
                output_vector = phi.system_function.algorithm(argument_vectors[0])
            case 2:
                output_vector = phi.system_function.algorithm(argument_vectors[0], argument_vectors[1])
            case _:
                log_error('Arity > 2 are not yet supported, sorry')
        log_debug(output_vector=output_vector)
        return output_vector



def parse_string_utf8(code):
    metamodel_source = None
    try:
        metamodel_source = pkg_resources.resource_string('naive', 'data/ba1_utf8.tx').decode('utf-8')
    except:
        with open(r'c:\users\David\pycharmprojects\naive\src\naive\data\ba1_utf8.tx', 'r',
                  encoding='utf-8') as source_file:
            metamodel_source = source_file.read()
    # log_debug(metamodel_source=metamodel_source)
    metamodel = metamodel_from_str(metamodel_source)
    model = metamodel.model_from_str(code)
    if model.token:
        formula = inflate_object(model)
        log_debug(parsed_formula=formula)
        return formula
    else:
        log_warning('Parsing result is empty.')


def inflate_object(model_object):
    arguments = []
    if hasattr(model_object, 'arguments'):
        for model_argument in model_object.arguments:
            argument = inflate_object(model_argument)
            arguments.append(argument)
    class_name = model_object._tx_fqn
    token = model_object.token
    # TODO: To scale this to multiple languages, implement a solution where
    #   every language is subscribed to the parsing function.
    match class_name:
        case 'BA1ConjunctionFormula':
            return f(BA1.conjunction, *arguments)
        case 'BA1DisjunctionFormula':
            return f(BA1.disjunction, *arguments)
        case 'BA1NegationFormula':
            return f(BA1.negation, *arguments)
        case 'BA1TruthFormula':
            # TODO: Question: use the system function directly or embed it into a formula?
            #return BA1.truth
            return f(BA1.truth)
        case 'BA1FalsumFormula':
            # TODO: Question: use the system function directly or embed it into a formula?
            #return BA1.falsum
            return f(BA1.falsum)
        case 'BA1AtomicVariableFormula':
            return av(BA1.b, token)


def parse_file_utf8():
    # TODO: Implement this.
    pass


set_default_scope('scope_1')
