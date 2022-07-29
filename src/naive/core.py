from __future__ import annotations
import collections.abc
import logging
import threading
import graphviz
import typing
import abc
from textx import metamodel_from_file, metamodel_from_str
import pkg_resources
import uuid

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


class Const:
    """A library of general-purpose pseudo-constants."""

    _BASE_KEY = 'base_key'
    _FACET_KEY = 'facets'
    _SCOPE_KEY = 'scope_key'
    _LANGUAGE_KEY = 'language_key'

    # SystemFunction Complementary Properties
    _DOMAIN = 'domain'
    _CODOMAIN = 'codomain'
    _ARITY = 'arity'
    _PYTHON_VALUE = 'python_value'

    _DEFAULT_SCOPE_KEY = ''
    _SYSTEM_DEFINED_KEY_PREFIX = 'sys_'
    _USER_DEFINED_KEY_PREFIX = 'ud1_'
    _LANGUAGE_NAIVE = 'naive'

    _QUALIFIED_KEY_SEPARATOR = '.'
    _MNEMONIC_KEY_ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789_'


class Facet(str):
    def __new__(
            cls,
            *args,
            inclusions: typing.Iterable[Facet] = None,
            exclusions: typing.Iterable[Facet] = None,
            **kwargs):
        """

        Definition:
        A facet is a class or a type or a category or a taxon of objects that delineates a meaningful set of objects based on their common properties and/or behaviors.
        Facets are not mutually exclusive by definition, but inclusivity or exclusivity constraints may be implemented to assure consistency with the data model.

        Args:
            inclusions (typing.Iterable[Facet]): Conditional: an iterable of facets that must be added whenever that facet is added.
            exclusions (typing.Iterable[Facet]): Conditional: an iterable of facets that must not be present whenever that facet included added.
        """
        facet = super().__new__(cls, *args, **kwargs)
        facet._inclusions = inclusions
        facet._exclusions = exclusions
        return facet

    @property
    def inclusions(self):
        return self._inclusions

    @property
    def exclusions(self):
        return self._exclusions


class Facets:

    scope = Facet('scope')

    language = Facet('language')

    domain = Facet('domain')

    function = Facet('function')

    atomic_property = Facet('atomic_property')

    formula = Facet('phi')
    """A mathematical phi.

    Definition:
    A phi, in the context of the naive package, is a tree of "calls" to functions, constants, and/or atomic variables.
    ...

    Different types of phi:
    - Atomic Variable (aka Unknown) (e.g. x + 5 = 17, x ∉ ℕ₀)
    - Formula Variable (e.g. φ = ¬x ∨ y, z ∧ φ)
    - n-ary SystemFunction Call with n in N0 (e.g. za1 abs)

    Different sub-types of n-ary Functions:
    - 0-ary Operator (aka Constant) (e.g. ba1_language truth)
    - Unary Operator (e.g. ba1_language negation)
    - Binary Operator (e.g. ba1_language conjunction)
    - n-ary SystemFunction

    """

    atomic_variable = Facet('formula_atomic_variable', inclusions=[formula])

    system_function = Facet('system_function')
    """Models a *mathematical* function that is implemented by a canonical *pythonic* (programmatic) function.

    Definition:
    A system function, in the context of the naive package,
    is a function that is predefined in the sense that it is accompanied by a programmatic algorithm and not a phi,
    and atomic in the sense that it cannot be further decomposed into constituent sub-formulae.

    """

    system_constant = Facet('atomic_constant', inclusions=[system_function])  # Aka a 0-ary function.
    system_unary_operator = Facet('atomic_unary_operator', inclusions=[system_function])  # Aka a unary function with operator notation.
    system_binary_operator = Facet('atomic_binary_operator', inclusions=[system_function])  # Aka a binary function with operator notation.
    system_n_ary_function = Facet('atomic_n_ary_function', inclusions=[system_function])

    system_function_call = Facet('system_function_call', inclusions=[formula])
    """A phi that is a call to a system (programmatic) function."""

    system_constant_call = Facet('formula_constant_call', inclusions=[system_function_call])  # Aka a 0-ary function.
    system_unary_operator_call = Facet('formula_unary_operator_call', inclusions=[system_function_call])
    system_binary_operator_call = Facet('formula_binary_operator_call', inclusions=[system_function_call])
    system_n_ary_function_call = Facet('formula_n_ary_function_call', inclusions=[system_function_call])

    # ST1

    set2 = Facet('set')

    finite_set = Facet('finite_set', inclusions=[set2])

    extensively_defined_finite_set = Facet('extensively_defined_finite_set', inclusions=[finite_set])
    """A finite set that is defined by the extensive list of its elements.
    
    Properties:
        * elements
    """

    infinite_set = Facet('infinite_set', inclusions=[set2])


def has_facet(o, facet):
    """Returns **True** if **o** has facet **facet**, **False** otherwise.

    Special case:
    Return **False** for pythonic objects that don't have a **facets** property."""
    return hasattr(o, 'facets') and facet in o.facets


def has_any_facet(o, facets):
    """Returns **True** if **o** has at least one **facet** among **facets**, **False** otherwise."""
    return True if o.facets.intersection(facets) else False


def add_facets(o, *args):
    """Add one or multiple facets to **o**, and enforce any related constraints such as automated inclusions."""
    args = Utils.flatten(args)
    for facet in args:
        o.facets.add(facet)
        if facet.inclusions is not None:
            for included_facet in facet.inclusions:
                add_facets(o, included_facet)
        # TODO: Implement exclusions. Note that it will be harder to keep it truly consistent.


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


class Log:
    """A library of logging and error handling functions and classes."""

    @staticmethod
    def set_debug_level():
        logging.root.setLevel(logging.DEBUG)

    @staticmethod
    def set_info_level():
        logging.root.setLevel(logging.INFO)

    @staticmethod
    def set_warning_level():
        logging.root.setLevel(logging.WARNING)

    @staticmethod
    def set_error_level():
        logging.root.setLevel(logging.ERROR)

    COERCION_SUCCESS = 1
    COERCION_FAILURE = 2

    code_exclusion_list = [1]

    @staticmethod
    def log_debug(message: str = '', code: int = 0, **kwargs):
        if code not in Log.code_exclusion_list:
            d = Utils.stringify_dictionary(**kwargs)
            message = f'DEBUGGING: {message} {d}.'
            logging.debug(message)

    USE_PRINT_FOR_INFO = True
    """Better output in Jupyter notebooks."""

    @staticmethod
    def log_info(message: str = '', code: int = 0, **kwargs):
        if code not in Log.code_exclusion_list:
            d = Utils.stringify_dictionary(**kwargs)
            message = f'{message} {d}'
            if Log.USE_PRINT_FOR_INFO:
                print(message)
            else:
                logging.info(message)

    class NaiveWarning(UserWarning):
        """The generic warning issued by the **naive** library."""
        pass

    @staticmethod
    def log_warning(message: str = '', code: int = 0, **kwargs):
        if code not in Log.code_exclusion_list:
            d = Utils.stringify_dictionary(**kwargs)
            message = f'WARNING: {message} {d}'
            logging.warning(message)

    class NaiveError(Exception):
        """The generic exception type raised by the **naive** library."""
        pass

    @staticmethod
    def log_error(message: str = '', *args, code: int = 0, **kwargs):
        if code not in Log.code_exclusion_list:
            d = Utils.stringify_dictionary(**kwargs)
            message = f'ERROR: {message}. {d}.'
            logging.error(message, exc_info=True)
            raise Log.NaiveError(message)


class Utils:
    """A library of miscellaneous utility classes and functions."""

    class Counter(object):
        def __init__(self):
            self.value = 1
            self._lock = threading.Lock()

        def get_value(self):
            with self._lock:
                self.value += 1
                return self.value

    @staticmethod
    def stringify_dictionary(**kwargs):
        s = ''
        for k, v in kwargs.items():
            s = f'{s}\n  {k}: {str(v)}'
        return s
        # return jsonpickle.encode(kwargs)

    @staticmethod
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
                Log.log_error(code=Log.COERCION_FAILURE, o=o, cls=cls)
            else:
                Log.log_debug(code=Log.COERCION_SUCCESS, o=o, cls=cls)
            return cls(o)

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
            # Recursive call for sub-elements
            # except strings that are understood as atomic in this context
            if isinstance(y, collections.abc.Iterable) and not isinstance(y, str):
                # We cannot call directly extend to support n-depth structures
                sub_flattened = Utils.flatten(*y)
                if sub_flattened is not None or not skip_none:
                    flattened.extend(sub_flattened)
            elif y is not None or not skip_none:
                flattened.append(y)
        return flattened

    def unkwargs(kwargs, key):
        return None if key not in kwargs else kwargs[key]

    def extract_scope_key_from_qualified_key(qualified_key):
        """Extract the scope_key key from a qualified key."""
        if qualified_key is None:
            return None
        else:
            qualified_key = str(qualified_key)
            first_separator_position = qualified_key.find(Const._QUALIFIED_KEY_SEPARATOR)
            return qualified_key[0, first_separator_position]

    def clean_mnemonic_key(mnemonic_key):
        if mnemonic_key is None:
            Log.log_error('NKey is None')
        else:
            mnemonic_key = str(mnemonic_key)
            return ''.join(c for c in mnemonic_key if c in Const._MNEMONIC_KEY_ALLOWED_CHARACTERS)


class Repr:
    """A library of functions and classes that help representing (or rendering, or visualizing) objects."""

    class ABCRepresentable(abc.ABC):
        """An abstract class for objects that support representation in multiple formats.

        See also:
            * :class:`PersistingRepresentable` class.
        """

        def __init__(self, *args, **kwargs):
            super().__init__()

        def __str__(self) -> str:
            # TODO: For future development, if images or other media are supported, the output of get_presentation() will need to be converted to text.
            return Repr.represent(self)

        def __repr__(self):
            return self.__str__()

        def __lt__(self, other):
            """Less Than.

            Allows sorting of variables by their names.
            Not to be confused with sorting variables by their values."""
            return str(self) < str(other)

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
                if isinstance(source, Repr.ABCRepresentable):
                    source_representable = source
                else:
                    source_string = str(source)

            source_representable = Utils.coerce(source_representable, Repr.ABCRepresentable)
            source_string = Utils.coerce(source_string, str)

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

        def imitate(self, o: Repr.ABCRepresentable):
            """Imitate the representation of another object."""
            for rformat in RFormats.CATALOG:
                # TODO: Minor design flaw: this process will also copy unsupported properties that default to UTF-8.
                self._representations[rformat] = Repr.represent(o, rformat)

    class Glyph(PersistingRepresentable):
        """A glyph is an elemental representation item."""

        def __init__(self, *args, **kwargs):
            """Initializes a Glyph object.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            super().__init__(*args, **kwargs)

    """Safe types for type coercion."""
    CoerciblePersistingRepresentable = typing.TypeVar(
        'CoerciblePersistingRepresentable',
        ABCRepresentable,
        bytes,  # Support for raw USASCII strings.
        PersistingRepresentable,
        str
    )

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
        representation = Utils.coerce(representation, str)
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

    def convert_formula_to_graphviz_digraph(phi: Core.Concept, digraph=None):
        title = Repr.represent(phi, RFormats.UTF8)
        id = phi.qualified_key

        if digraph is None:
            digraph = graphviz.Digraph(id)

        digraph.node(id, title)
        if has_facet(phi, Facets.formula) and isinstance(phi.arguments, collections.abc.Iterable):
            for argument in phi.arguments:
                Repr.convert_formula_to_graphviz_digraph(phi=argument, digraph=digraph)
                digraph.edge(id, argument.qualified_key, dir='back')

        return digraph

    def convert_formula_to_dot(phi: Core.Concept):
        if not has_facet(phi, Facets.formula):
            Log.log_error('Missing phi facet', phi=phi)
        digraph = Repr.convert_formula_to_graphviz_digraph(phi=phi)
        return digraph.source

    def render_formula_as_ipython_mimebundle(phi: Core.Concept):
        """
        Render the phi as a digraph in SVG format,
        in Jupyter Notebook, Jupyter QT Console, and/or insider Spyder IDE.

        Bibliography:
            * https://graphviz.readthedocs.io/en/stable/api.html#graphviz.Graph._repr_mimebundle_
            * https://graphviz.readthedocs.io/en/stable/manual.html
        """
        if not has_facet(phi, Facets.formula):
            Log.log_error('Missing phi facet', phi=phi)
        digraph = Repr.convert_formula_to_graphviz_digraph(phi=phi)
        digraph._repr_mimebundle_()

    @staticmethod
    def represent(
            o: object,
            rformat: str = None,
            *args,
            left_bracket=None,
            right_bracket=None,
            element_separator=None,
            **kwargs) -> str:
        """Get the object'representation representation in the desired format.

        Args:
            o (object): The object to be represented.
            rformat (str): The representation format.

        Returns:
            The object's representation, if supported in the desired format.
        """
        if o is None:
            # If nothing is passed for representation,
            # we return an empty string to facilitate concatenations.
            return ''
        if rformat is None:
            # Default rformat.
            rformat = RFormats.DEFAULT
        if has_facet(o, Facets.atomic_variable):
            # Basic symbol representation.
            # x
            # TODO: Modify approach. Storing and returning the _base_name like this
            #   prevent support for other mathematical fonts, such as MathCal, etc.
            #   As an initial approach, it provides support for ASCII like variables.
            #   We may consider storing a Glyph as the base name,
            #   and calling the static represent() function.
            return o._base_name + \
                   Repr.subscriptify(Repr.represent(o._indexes, rformat), rformat)
        elif has_facet(o, Facets.system_constant_call):
            # x
            return f'{Repr.represent(o._system_function, rformat)}'
        elif has_facet(o, Facets.system_unary_operator_call):
            # fx
            return f'{Repr.represent(o._system_function, rformat)}{Repr.represent(o.arguments[0], rformat)}'
        elif has_facet(o, Facets.system_binary_operator_call):
            # (x f y)
            return f'{Repr.represent(Glyphs.parenthesis_left, rformat)}{Repr.represent(o.arguments[0], rformat)}{Repr.represent(Glyphs.small_space, rformat)}{Repr.represent(o._system_function, rformat)}{Repr.represent(Glyphs.small_space, rformat)}{Repr.represent(o.arguments[1], rformat)}{Repr.represent(Glyphs.parenthesis_right, rformat)}'
        elif has_facet(o, Facets.system_n_ary_function_call):
            # f(x,y,z)
            variable_list = ', '.join(map(lambda a: Repr.represent(a), o.arguments))
            return f'{Repr.represent(o._system_function, rformat)}{Repr.represent(Glyphs.parenthesis_left, rformat)}{variable_list}{Repr.represent(Glyphs.parenthesis_right, rformat)}'
        elif has_facet(o, Facets.extensively_defined_finite_set):
            return o._base_name + \
                   Repr.subscriptify(Repr.represent(o._indexes, rformat), rformat)
        elif hasattr(o, '_' + rformat) or hasattr(o, '_' + RFormats.DEFAULT):
            # TODO: Question: Used by facet=domain, facet=system_function, etc.
            #   Don't feel 100% sure this is the correct approach, we would be
            #   better off reusing a Glyph as a property when available.
            if hasattr(o, '_' + rformat):
                return getattr(o, '_' + rformat)
            elif hasattr(o, '_' + RFormats.DEFAULT):
                # We fall back on UTF-8
                return getattr(o, '_' + RFormats.DEFAULT)
            else:
                Log.log_error('Missing rformat property', rformat=rformat, __dict__=o.__dict__)
        elif hasattr(o, '_representations'):
            Log.log_warning('Obsolete representation method with _representations property ?', rformat=rformat, __dict__=o.__dict__)
            if rformat in o._representations:
                return o._representations[rformat]
            elif RFormats.UTF8 in o._representations:
                # We fall back on UTF-8
                return o._representations[RFormats.UTF8]
            else:
                Log.log_error('Missing rformat in _representations', rformat=rformat, __dict__=o.__dict__)
        elif not isinstance(o, Core.Concept):
            # The final fallback method before raising an error.
            # Provides support for all base types and non-naive classes.
            # Note that we exclude Core.Concept from the above
            # condition to avoid infinite ping-pong plays between
            # __str__ and represent().
            return str(o)
        else:
            Log.log_error('No representation solution',
                          type=type(o),
                          rformat=rformat,
                          facets = o.facets if hasattr(o, 'facets') else None,
                          __dict__=o.__dict__)

    @staticmethod
    def represent_declaration(o: object, rformat: str = None, *args, **kwargs) -> str:
        if has_facet(o, Facets.atomic_variable):
            if rformat is None:
                rformat = RFormats.DEFAULT
            match rformat:
                case RFormats.UTF8:
                    return f'With {Repr.represent(o, rformat)} ∈ {Repr.represent(o.codomain, rformat)}.'
                case _:
                    raise NotImplementedError('TODO')
        if has_facet(o, Facets.extensively_defined_finite_set):
            if rformat is None:
                rformat = RFormats.DEFAULT
            match rformat:
                case RFormats.UTF8:
                    element_list = ', '.join(map(lambda a: Repr.represent(a, rformat), o.elements))
                    return f'Let {Repr.represent(o, rformat)} := {Repr.represent(Glyphs.curly_bracket_left, rformat)}{element_list}{Repr.represent(Glyphs.curly_bracket_right, rformat)}'
                case _:
                    raise NotImplementedError('TODO')
        else:
            Log.log_error(f'Declaration is not supportted for these facets.',
                          facets=o.facets,
                          qualified_key=o.qualified_key, rformat=rformat)


class Glyphs:
    # Number sets
    standard_0 = Repr.Glyph(utf8='0', latex=r'0', html='0', usascii='0')
    standard_1 = Repr.Glyph(utf8='1', latex=r'1', html='1', usascii='1')
    standard_x_lowercase = Repr.Glyph(utf8='v', latex=r'v', html='v', usascii='v')
    standard_y_lowercase = Repr.Glyph(utf8='y', latex=r'y', html='y', usascii='y')
    standard_z_lowercase = Repr.Glyph(utf8='z', latex=r'z', html='z', usascii='z')
    mathbb_a_uppercase = Repr.Glyph(utf8='𝔸', latex=r'\mathbb{A}', html='&Aopf;', usascii='A')
    mathbb_b_uppercase = Repr.Glyph(utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
    mathbb_n_uppercase = Repr.Glyph(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', usascii='N')
    mathbb_z_uppercase = Repr.Glyph(utf8='ℤ', latex=r'\mathbb{Z}', html='&Zopf;', usascii='Z')
    # {\displaystyle \mathbb {C} }\mathbb{C} 	ℂ	Complex number	\mathbb{C}, \Complex	&Copf;	U+2102
    # {\displaystyle \mathbb {H} }\mathbb {H} 	ℍ	Quaternion	\mathbb{H}, \H	&quaternions;	U+210D
    # {\displaystyle \mathbb {O} }\mathbb {O} 	𝕆	Octonion	\mathbb{O}	&Oopf;	U+1D546
    # {\displaystyle \mathbb {Q} }\mathbb {Q} 	ℚ	Rational number	\mathbb{Q}, \Q	&Qopf;	U+211A
    # {\displaystyle \mathbb {R} }\mathbb {R} 	ℝ	Real number	\mathbb{R}, \R	&Ropf;	U+211D
    # {\displaystyle \mathbb {S} }\mathbb {S} 	𝕊	Sedenion	\mathbb{S}	&Sopf;	U+1D54A

    to = Repr.Glyph(utf8='⟶', latex=r'\longrightarrow', html=r'&rarr;', usascii='-->')
    maps_to = Repr.Glyph(utf8='⟼', latex=r'\longmapsto', html=r'&mapsto;', usascii='|->')
    colon = Repr.Glyph(utf8=':', latex=r'\colon', html=r':', usascii=':')

    # Bibliography:
    #   * https://en.wikipedia.org/wiki/List_of_logic_symbols
    logical_falsum = Repr.Glyph(utf8='⊥', latex=r'\bot', html='&perp;', usascii='F')
    logical_truth = Repr.Glyph(utf8='⊤', latex=r'\top', html='&top;', usascii='T')
    logical_negation = Repr.Glyph(utf8='¬', latex=r'\lnot', html='&not;', usascii='not')
    logical_conjunction = Repr.Glyph(utf8='∧', latex=r'\land', html='&and;', usascii='and')
    logical_disjunction = Repr.Glyph(utf8='∨', latex=r'\lor', html='&or;', usascii='or')
    logical_material_implication = Repr.Glyph(utf8='⇒', latex=r'\implies', html='&rArr;', usascii='implies')
    logical_material_equivalence = Repr.Glyph(utf8='⇔', latex=r'\iif', html='&hArr;', usascii='iif')

    # Greek Letters
    phi_plain_small = Repr.Glyph(utf8='φ', latex=r'\phi', html='&phi;', usascii='phi')
    phi_plain_cap = Repr.Glyph(utf8='Φ', latex=r'\Phi', html='&Phi;', usascii='Phi')
    psi_plain_small = Repr.Glyph(utf8='ψ', latex=r'\psi', html='&psi;', usascii='psi')
    psi_plain_cap = Repr.Glyph(utf8='Ψ', latex=r'\Psi', html='&Psi;', usascii='Psi')

    # Brackets
    # Sources:
    #   * https://en.wikipedia.org/wiki/Bracket
    parenthesis_left = Repr.Glyph(utf8='(', latex=r'\left(', html='&lparen;', usascii='(')
    parenthesis_right = Repr.Glyph(utf8=')', latex=r'\right)', html='&rparen;', usascii=')')
    square_bracket_left = Repr.Glyph(utf8='[', latex=r'\left[', html='&91;', usascii='[')
    square_bracket_right = Repr.Glyph(utf8=']', latex=r'\right]', html='&93;', usascii=']')
    curly_bracket_left = Repr.Glyph(utf8='{', latex=r'\left\{', html='&123;', usascii='{')
    curly_bracket_right = Repr.Glyph(utf8='}', latex=r'\right\}', html='&125;', usascii='}')
    angle_bracket_left = Repr.Glyph(utf8='⟨', latex=r'\left\langle', html='&lang;', usascii='<')
    angle_bracket_right = Repr.Glyph(utf8='⟩', latex=r'\right\rangle', html='&rang;', usascii='>')

    # Set Theory
    element_of = Repr.Glyph(utf8='∈∉', latex=r'\in')
    not_element_of = Repr.Glyph(utf8='∉', latex=r'\notin')

    # Spaces
    small_space = Repr.Glyph(utf8=' ', latex=r'\,', html='&nbsp;', usascii=' ')


def set_unique_scope() -> str:
    """Creates a new, unique user-defined scope, and set it as the current default scope.

    To avoid scope collisions, the unique key is generated as a UUID using the uuid.uuid4() function. The dot ('.') characters are then replaced by underscores ('_') to avoid syntaxic confusion, the dot ('.') being used as the namespace separator.

    Returns:
        str: The new scope key.
        """
    user_defined_scope_key = Const._USER_DEFINED_KEY_PREFIX + str(uuid.uuid4()).replace('-', '_')
    return set_default_scope(user_defined_scope_key)


def set_default_scope(scope_key):
    """Sets the default user-defined scope. Creates it if necessary.

    Args:
        scope_key (str): A key to identify that user-defined scope.

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
        Log.log_error(
            f'None is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{Const._MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    if not isinstance(scope_key, str):
        Log.log_error(
            f'The object "{scope_key}" of type "{type(scope_key)}" is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{Const._MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    scope_key_cleaned = Utils.clean_mnemonic_key(scope_key)
    if scope_key_cleaned != scope_key:
        Log.log_warning(
            f'Please note that the context key "{scope_key}" contained unsupported characters. The allowed characters for context keys are: "{Const._MNEMONIC_KEY_ALLOWED_CHARACTERS}". It was automatically cleaned from unsupported characters. The resulting context key is: {scope_key_cleaned}')
    if scope_key == '':
        Log.log_error(
            f'An empty string is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{Const._MNEMONIC_KEY_ALLOWED_CHARACTERS}".')

    prefixed_key = Const._USER_DEFINED_KEY_PREFIX + scope_key_cleaned
    _DEFAULT_SCOPE_KEY = prefixed_key
    Log.log_info(f'Default scope_key: {scope_key_cleaned}')


def get_default_scope():
    return _DEFAULT_SCOPE_KEY[len(Const._USER_DEFINED_KEY_PREFIX):]


def av(codomain, base_name=None, indexes=None):
    """Shorthand alias for :ref:`declare_atomic_variable` **declare_atomic_variable**."""
    return Core.declare_atomic_variable(codomain, base_name, indexes)


def f(o, *args):
    """Shorthand function to write a phi."""
    return Core.write_formula(o, *args)


def get_qualified_key(scope_key, language_key, base_key):
    return f'{scope_key}{Const._QUALIFIED_KEY_SEPARATOR}{language_key}{Const._QUALIFIED_KEY_SEPARATOR}{base_key}'


_concept_database = {}
"""The static database of concepts."""

_token_database = {}
"""The static database of tokens."""


class Core:
    class Concept:

        global _concept_database
        global _token_database

        def __init__(self, scope_key, language_key, base_key,
                     facets,
                     utf8=None, latex=None, html=None, usascii=None, tokens=None,
                     base_name=None, indexes=None,
                     domain=None, codomain=None, arity=None, python_value=None,
                     arguments=None, algorithm=None, elements=None,
                     system_function=None,
                     **kwargs):
            # Identification Properties that constitute the Qualified Key.
            if scope_key is None:
                scope_key = get_default_scope()
            self._scope_key = Utils.clean_mnemonic_key(scope_key)
            self._language_key = Utils.clean_mnemonic_key(language_key)
            self._base_key = Utils.clean_mnemonic_key(base_key)
            # Structural properties
            self._facets = set()
            # Recall add_facets to assure that facet logic is applied.
            add_facets(self, facets)
            # Representation Properties
            self._utf8 = utf8
            self._latex = latex
            self._html = html
            self._usascii = usascii
            self._base_name = base_name
            self._indexes = indexes
            self._tokens = tokens
            # Other properties
            self._arguments = arguments
            self._arity = arity
            self._domain = domain
            self._codomain = codomain
            self._algorithm = algorithm
            self._elements = elements
            self._system_function = system_function
            self._python_value = python_value
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
                        Log.log_error(
                            f'The "{token}" token was already in the token static database. We need to implement a priority algorithm to manage these situations.',
                            token=token, self=self)
            # Append the concept in the database
            if self.qualified_key not in _concept_database:
                _concept_database[self.qualified_key] = self
            else:
                Log.log_error(
                    'The initialization of the concept could not be completed because the qualified key was already present in the static database.',
                    qualified_key=self.qualified_key)

        def __str__(self):
            return Repr.represent(self, RFormats.UTF8)

        def __repr__(self):
            return Repr.represent(self, RFormats.UTF8)

        @property
        def algorithm(self):
            """function: The *python* function that implements the canonical algorithm for that *mathematical* function.

            Facets:
                * system_function
            """
            return self._algorithm

        @property
        def arity(self):
            return self._arity

        @property
        def arguments(self):
            """The list of arguments linked to a phi.

            Facets:
                * phi"""
            return self._arguments

        @property
        def base_name(self):
            return self._base_name

        @property
        def base_key(self):
            return self._base_key

        @staticmethod
        def check_concept_from_decomposed_key(scope_key: str, language_key: str, base_key: str,
                                              **kwargs):
            if scope_key is not None and language_key is not None and base_key is not None:
                qualified_key = get_qualified_key(scope_key, language_key, base_key)
                return Core.Concept.check_concept_from_qualified_key(
                    qualified_key, scope=scope_key, language=language_key, base_key=base_key,
                    **kwargs)
            else:
                Log.log_error('Some identification properties are None',
                              scope=scope_key, language=language_key, base_key=base_key, **kwargs)

        @staticmethod
        def check_concept_from_qualified_key(qualified_key, **kwargs):
            if qualified_key is not None:
                return qualified_key in _concept_database
            else:
                Log.log_error('Checking concept with None qualified key is impossible.',
                              qualified_key=qualified_key, **kwargs)

        @property
        def codomain(self):
            """The codomain of a function.

            Constants are 0-ary functions. Hence, they do not have a domain property but do have a codomain property, in the sense that a constant 'outputs' a value which must pertain a domain."""
            return self._codomain

        @property
        def domain(self):
            return self._domain

        @property
        def elements(self):
            """The elements of an extensively defined finite set.

            By definition, extensively defined finite sets are defined as the extensive list of their elements. This property exposes this list.

            For obvious programmatic reasons, this property is not exposed for infite sets and sets that are potentially too large.

            Facets:
                * extensively_defined_finite_set
            """
            return self._elements

        @property
        def facets(self) -> str:
            return self._facets

        @staticmethod
        def get_concept_from_decomposed_key(scope_key: str, language_key: str, base_key: str,
                                            **kwargs):
            if scope_key is not None and language_key is not None and base_key is not None:
                qualified_key = get_qualified_key(scope_key, language_key, base_key)
                return Core.Concept.get_concept_from_qualified_key(
                    qualified_key, scope=scope_key, language=language_key, base_key=base_key,
                    **kwargs)
            else:
                Log.log_error('Some identification properties are None',
                              scope=scope_key, language=language_key, base_key=base_key, **kwargs)

        @staticmethod
        def get_concept_from_qualified_key(qualified_key, **kwargs):
            if qualified_key is not None:
                if qualified_key in _concept_database:
                    return _concept_database[qualified_key]
                else:
                    return Core.Concept(qualified_key=qualified_key, **kwargs)
            else:
                Log.log_error('Getting concept with None qualified key is impossible.',
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

        @property
        def indexes(self):
            return self._indexes

        def is_equal_concept(self, other: Core.Concept):
            return self.qualified_key == other.qualified_key

        @property
        def language(self):
            return self._language_key

        @property
        def python_value(self):
            return self._python_value

        @property
        def system_function(self):
            return self._system_function

        @property
        def qualified_key(self):
            return get_qualified_key(scope_key=self.scope_key,
                                     language_key=self.language,
                                     base_key=self.base_key)

        @property
        def scope_key(self):
            return self._scope_key

        @property
        def tokens(self):
            return self._tokens

    # Scope.
    system_scope = Concept(
        scope_key='sys', language_key=Const._LANGUAGE_NAIVE, base_key='sys',
        facets=[Facets.scope],
        utf8='sys', latex=r'\text{sys}', html='sys', usascii='sys')

    # TODO: Check that we do create a new scope object whenever we set the scope.
    initial_user_defined_scope = Concept(
        scope_key='sys', language_key=Const._LANGUAGE_NAIVE,
        facets=[Facets.scope],
        base_key=Const._USER_DEFINED_KEY_PREFIX + 'scope_1',
        utf8='scope_key₁', latex=r'\text{scope_key}_1', html=r'scope_key<sub>1</sub>', usascii='scope1')

    class SystemFunction(Concept):

        def __init__(
                self,
                # Identification properties
                scope_key, language_key, base_key,
                facets,
                # Mandatory complementary properties
                codomain, algorithm,
                # Conditional complementary properties
                domain=None, arity=None, python_value=None,
                # Representation properties
                utf8=None, latex=None, html=None, usascii=None, tokens=None,
                **kwargs):
            super().__init__(
                scope_key=scope_key, language_key=language_key, base_key=base_key,
                facets=facets,
                utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
                arity=arity, codomain=codomain, python_value=python_value,
                algorithm=algorithm,
                **kwargs)
            add_facets(self, Facets.system_function)


    @staticmethod
    def compute_programmatic_value(x: Concept):
        # TODO: The idea is to distinguish the computerized or programmatic value,
        #   here as a canonical mapping to a python object,
        #   with the symbolic value, the later being the naive concept.
        if has_facet(x, Facets.system_constant):
            return x._python_value
        else:
            raise NotImplementedError('Missing system_constant and/or python_value property', x=x)

    @staticmethod
    def equal_programmatic_value(x: Concept, y: (Concept, object)):
        """Returns **True** if **x**'s programmatic value is equal to **y**'s programmatic value."""
        return Core.compute_programmatic_value(x) == Core.compute_programmatic_value(y)

    _FORMULA_AUTO_COUNTER = Utils.Counter()

    @staticmethod
    def list_formula_atomic_variables(phi):
        """Return the sorted set of variables present in the phi, and its subformulae recursively."""
        atomic_variables = set()
        if phi.arguments is not None:
            for argument in phi.arguments:
                if has_facet(argument, Facets.atomic_variable):
                    atomic_variables.add(argument)
                elif has_facet(argument, Facets.formula):
                    atomic_variables_prime = Core.list_formula_atomic_variables(argument)
                    for argument_prime in atomic_variables_prime:
                        atomic_variables.add(argument_prime)
                else:
                    Log.log_error('Not implemented yet', argument=argument, phi=phi)

        # To allow sorting and indexing, convert the set to a list.
        atomic_variables = list(atomic_variables)
        atomic_variables.sort(key=lambda x: x.base_key)
        return atomic_variables

    @staticmethod
    def write_formula(o, *args):
        global _FORMULA_AUTO_COUNTER
        scope_key = _DEFAULT_SCOPE_KEY
        index = Core._FORMULA_AUTO_COUNTER.get_value()
        base_key = 'f' + str(index)
        system_function = None
        facets = None
        arity = None

        if facets is None:
            facets = set()
        # Adding the phi facet is unecessary because
        # the phi-like facet will add it by automatic inclusions.
        # I nevertheless add it for code clarity.
        facets.add(Facets.formula)

        if has_facet(o, Facets.system_function):
            system_function = o
            arity = system_function.arity
            codomain = system_function.codomain
            if has_facet(o, Facets.system_constant):
                facets.add(Facets.system_constant_call)
            elif has_facet(o, Facets.system_unary_operator):
                facets.add(Facets.system_unary_operator_call)
            elif has_facet(o, Facets.system_binary_operator):
                facets.add(Facets.system_binary_operator_call)
                # TODO: Implement all other possibilities
        arguments = args
        formula = Core.Concept(
            # Identification properties
            scope_key=scope_key, language_key=Const._LANGUAGE_NAIVE, base_key=base_key,
            # Structural properties
            facets=facets,
            # Conditional complementary properties
            system_function=system_function, arguments=arguments,
            arity=arity, codomain=codomain
        )
        Log.log_info(Repr.represent(formula))
        return formula

    @staticmethod
    def declare_atomic_variable(codomain, base_name=None, indexes=None):
        # TODO: Provide support for different math fonts (e.g.: https://www.overleaf.com/learn/latex/Mathematical_fonts)
        # TODO: Provide support for indexed variables. Variable declaration should be possible with indexes bounds and not only with individual indexes values.
        # Identification properties
        scope_key = _DEFAULT_SCOPE_KEY
        language_key = Const._LANGUAGE_NAIVE
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
        # Structural properties
        if Core.Concept.check_concept_from_decomposed_key(
                scope_key=scope_key, language_key=language_key, base_key=base_key):
            variable = Core.Concept.get_concept_from_decomposed_key(
                scope_key=scope_key, language_key=language_key, base_key=base_key)
            # TODO: Assert that variable concept is of facet variable
            Log.log_warning(
                'This variable is already declared. In consequence, the existing variable is returned, instead of declaring a new one.',
                variable=variable, scope_key=scope_key, base_key=base_key)
            return variable
        else:
            arity = 0
            variable = Core.Concept(
                scope_key=scope_key, language_key=language_key, base_key=base_key,
                facets=Facets.atomic_variable,
                codomain=codomain, base_name=base_name, indexes=indexes, arity=arity)
            Log.log_info(Repr.represent_declaration(variable))
            return variable


# TODO: Question: what should be the scope_key of user defined scopes? sys? the scope_key itself?


class BA1:
    """The **Boolean Algebra 1** library.

    This library generates the mathematical objects that composes the basic Boolean algebra.
    """
    # TODO: Develop a metaclass for "Language" classes.

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
    ba1_scope = Core.Concept(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='ba1_scope',
        facets=Facets.scope,
        utf8='ba1_scope', latex=r'\text{ba1_scope}', html='ba1_scope', usascii='ba1_scope')

    # Language.
    ba1_language = Core.Concept(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='ba1_language',
        facets=Facets.language,
        utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

    # Domains.
    b = Core.Concept(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='b',
        facets=Facets.domain,
        utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
    b2 = Core.Concept(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='b2',
        facets=Facets.domain,
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
        v = Utils.flatten(v)  # If scalar, convert to list.
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
        v1 = Utils.flatten(v1)  # If scalar, convert to list.
        v2 = Utils.flatten(v2)  # If scalar, convert to list.
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
        v1 = Utils.flatten(v1)  # If scalar, convert to list.
        v2 = Utils.flatten(v2)  # If scalar, convert to list.
        return [BA1.truth if (b1 == BA1.truth or b2 == BA1.truth) else BA1.falsum for b1, b2 in zip(v1, v2)]

    # Functions.
    truth = Core.SystemFunction(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='truth',
        facets=[Facets.function, Facets.system_function, Facets.system_constant],
        codomain=b, algorithm=truth_algorithm,
        utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
        arity=0, python_value=True)

    falsum = Core.SystemFunction(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='falsum',
        facets=[Facets.function, Facets.system_function, Facets.system_constant],
        codomain=b, algorithm=falsum_algorithm,
        utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
        arity=0, python_value=False)

    negation = Core.SystemFunction(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='negation',
        facets=[Facets.function, Facets.system_function, Facets.system_unary_operator],
        codomain=b, algorithm=negation_algorithm,
        utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
        domain=b, arity=1)

    conjunction = Core.SystemFunction(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='conjunction',
        facets=[Facets.function, Facets.system_function, Facets.system_binary_operator],
        codomain=b, algorithm=conjunction_algorithm,
        utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
        domain=b, arity=2)

    disjunction = Core.SystemFunction(
        scope_key=_SCOPE_BA1, language_key=_LANGUAGE_BA1, base_key='disjunction',
        facets=[Facets.function, Facets.system_function, Facets.system_binary_operator],
        codomain=b, algorithm=disjunction_algorithm,
        utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
        domain=b, arity=2)

    @staticmethod
    def get_bn_domain(n):
        """Returns the n-tuple codomain 𝔹ⁿ where n is a natural number > 0.

        Assures the presence of the codomain 𝔹ⁿ in the concept database.
        """
        if not isinstance(n, int):
            Log.log_error('n must be an int')
        elif n < 1:
            Log.log_error('n must be > 1')
        elif n == 1:
            return BA1.b
        elif n == 2:
            return BA1.b2
        else:
            scope_key = BA1._SCOPE_BA1
            facets = [Facets.domain]
            language_key = BA1._LANGUAGE_BA1
            base_key = 'b' + str(n)  # TODO: Check it is an int
            # TODO: Consider implementing a lock to avoid bugs with multithreading when checking the static dictionary
            if Core.Concept.check_concept_from_decomposed_key(
                    scope_key=scope_key, language_key=language_key, base_key=base_key):
                return Core.Concept.get_concept_from_decomposed_key(
                    scope_key=scope_key, language_key=language_key, base_key=base_key)
            else:
                return Core.Concept(
                    scope_key=scope_key, language_key=language_key, base_key=base_key,
                    facets=facets,
                    utf8='𝔹' + Repr.superscriptify(n), latex=r'\mathbb{B}^{' + str(n) + r'}',
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
    def satisfaction_index(phi: Core.Concept, variables_list=None):
        """Compute the **satisfaction indexes** (:math:`\text{sat}_I`) of a Boolean phi (:math:`\phi`).

        Alias:
        **sat_i**

        Definition:
        Let :math:`\phi` be a Boolean phi.
        :math:`\text{sat}_I \colon= ` the truth value of :math:`\phi` in all possible worlds.

        Args:
            phi (BooleanFormula): The Boolean phi :math:`\phi` .
        """
        # Retrieve the computed results
        # TODO: Check that all phi are Boolean phi. Otherwise, the phi
        #   may not return a Boolean value, forbidding the computation of a satisfaction set.
        if variables_list is None:
            variables_list = Core.list_formula_atomic_variables(phi)
        variables_number = len(variables_list)
        arguments_number = phi.arity
        argument_vectors = [None] * arguments_number
        Log.log_debug(arguments_number=arguments_number)
        for argument_index in range(0, arguments_number):
            argument = phi.arguments[argument_index]
            Log.log_debug(
                argument=argument,
                argument_index=argument_index,
                argument_type=type(argument),
                argument_codomain=argument.codomain,
                argument_facets=argument.facets)
            if has_facet(argument, Facets.system_function_call) and \
                    argument.codomain == BA1.b:
                # This argument is a Boolean Formula.
                Log.log_debug('This argument is a Boolean Formula')
                # Recursively compute the satisfaction set of that phi,
                # restricting the variables list to the subset of necessary variables.
                vector = BA1.satisfaction_index(argument, variables_list=variables_list)
                argument_vectors[argument_index] = vector
            elif has_facet(argument, Facets.atomic_variable) and \
                    argument.codomain == BA1.b:
                # This argument is a Boolean atomic proposition.
                Log.log_debug('This argument is a Boolean atomic proposition')
                # We want to retrieve its values from the corresponding bit combinations column.
                # But we need the vector to be relative to variables_list.
                # Thus we must first find the position of this atomic variable,
                # in the variables_list.
                atomic_variable_index = variables_list.index(argument)
                vector = BA1.get_boolean_combinations_column(variables_number, atomic_variable_index)
                Log.log_debug(vector=vector)
                argument_vectors[argument_index] = vector
            else:
                Log.log_error('Unexpected type',
                              argument=argument, t=type(argument), facets=argument.facets,
                              codomain=argument.codomain)
        Log.log_debug(argument_vectors=argument_vectors)
        output_vector = None
        Log.log_debug(phi=phi, arity=phi.arity, system_function=phi.system_function)
        match phi.arity:
            case 0:
                output_vector = phi.system_function.algorithm(vector_size=2 ** variables_number)
            case 1:
                output_vector = phi.system_function.algorithm(argument_vectors[0])
            case 2:
                output_vector = phi.system_function.algorithm(argument_vectors[0], argument_vectors[1])
            case _:
                Log.log_error('Arity > 2 are not yet supported, sorry')
        Log.log_debug(output_vector=output_vector)
        return output_vector


class ST1:
    """The **Set Theory 1** library."""
    # TODO: Develop a metaclass for "Language" classes.

    _SCOPE_ST1 = 'sys_st1'
    _LANGUAGE_ST1 = 'ba1_language'

    # Scope.
    st1_scope = Core.Concept(
        scope_key=_SCOPE_ST1, facets=Facets.scope, language_key=_LANGUAGE_ST1, base_key='st1_scope',
        utf8='st1_scope', latex=r'\text{st1_scope}', html='st1_scope', usascii='st1_scope')

    # Language.
    st1_language = Core.Concept(
        scope_key=_SCOPE_ST1, facets=Facets.language, language_key=_LANGUAGE_ST1, base_key='st1_language',
        utf8='st1_language', latex=r'\text{st1_language}', html='st1_language', usascii='st1_language')

    @staticmethod
    def declare_finite_set(base_name=None, indexes=None, elements=None, scope=None):
        # TODO: Provide support for a relative parent (aka universal) set, and enforce consistency of elements.
        # TODO: Provide support for different math fonts (e.g.: https://www.overleaf.com/learn/latex/Mathematical_fonts)
        # TODO: Provide support for indexed variables. Variable declaration should be possible with indexes bounds and not only with individual indexes values.
        # Identification properties
        scope_key = _DEFAULT_SCOPE_KEY
        language_key = Const._LANGUAGE_NAIVE
        if base_name is None:
            # TODO: Make this a scope preference setting, letting the user choose the default
            #   variable base_name in that scope.
            base_name = 'S'
            # TODO: automate index attribution if indexes is not provided.
        base_key = base_name
        if indexes is not None:
            if not isinstance(indexes, collections.abc.Iterable):
                base_key = base_key + '__' + str(indexes)
            else:
                base_key = base_key + '__' + '_'.join(str(index) for index in indexes)
        # Structural properties
        if Core.Concept.check_concept_from_decomposed_key(
                scope_key=scope_key, language_key=language_key, base_key=base_key):
            finite_set = Core.Concept.get_concept_from_decomposed_key(
                scope_key=scope_key, language_key=language_key, base_key=base_key)
            # TODO: Assert that variable concept is of facet variable
            Log.log_warning(
                'This finite set is already declared. In consequence, the existing variable is returned, instead of declaring a new one.',
                finite_set=finite_set, scope_key=scope_key, base_key=base_key)
            return finite_set
        else:
            finite_set = Core.Concept(
                scope_key=scope_key, language_key=language_key, base_key=base_key,
                facets=Facets.extensively_defined_finite_set,
                utf8=base_name,
                base_name=base_name, indexes=indexes, elements=elements)
            Log.log_info(Repr.represent_declaration(finite_set))
            return finite_set


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
        Log.log_debug(parsed_formula=formula)
        return formula
    else:
        Log.log_warning('Parsing result is empty.')


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
            # TODO: Question: use the system function directly or embed it into a phi?
            # return BA1.truth
            return f(BA1.truth)
        case 'BA1FalsumFormula':
            # TODO: Question: use the system function directly or embed it into a phi?
            # return BA1.falsum
            return f(BA1.falsum)
        case 'BA1AtomicVariableFormula':
            return av(BA1.b, token)


def parse_file_utf8():
    # TODO: Implement this.
    pass


set_unique_scope()
