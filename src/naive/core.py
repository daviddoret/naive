from __future__ import annotations
import log
from _function_subscriptify import subscriptify
from _function_superscriptify import superscriptify
import threading

# Concept Core Properties
import rformats
import glyphs

_BASE_KEY = 'base_key'
_STRUCTURE_KEY = 'structure_key'
_SCOPE_KEY = 'scope_key'
_LANGUAGE_KEY = 'language_key'

# SystemFunction Complementary Properties
_DOMAIN = 'domain'
_CODOMAIN = 'codomain'
_ARITY = 'arity'
_PYTHON_VALUE = 'python_value'

# NType Keys
_STRUCTURE_SCOPE = 'scope'
_STRUCTURE_LANGUAGE = 'language'
_STRUCTURE_DOMAIN = 'domain'
_STRUCTURE_FUNCTION = 'function'
_STRUCTURE_ATOMIC_PROPERTY = 'ap'
_STRUCTURE_VARIABLE = 'variable'
_STRUCTURE_FORMULA = 'formula'

_QUALIFIED_KEY_SEPARATOR = '.'
_MNEMONIC_KEY_ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz012345679_'

_DEFAULT_SCOPE_KEY = ''
_SYSTEM_DEFINED_KEY_PREFIX = 'sys_'
_USER_DEFINED_KEY_PREFIX = 'ud_'
_LANGUAGE_NAIVE = 'naive'


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
        log.error('NKey is None')
    else:
        mnemonic_key = str(mnemonic_key)
        return ''.join(c for c in mnemonic_key if c in _MNEMONIC_KEY_ALLOWED_CHARACTERS)


class Concept:
    _concept_database = {}
    """The static database of concepts."""

    _token_database = {}
    """The static database of tokens."""

    def __init__(self, scope_key, structure_key, language_key, base_key,
                 utf8=None, latex=None, html=None, usascii=None, tokens=None,
                 domain=None, codomain=None, arity=None, pythong_value=None,
                 **kwargs):
        # Identification Properties that constitute the Qualified Key.
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
                if token not in Concept._concept_database:
                    # TODO: Question: should we store a reference to the Concept or store the Concept qualified key?
                    Concept._concept_database[token] = self
                else:
                    log.error(
                        f'The "{token}" token was already in the token static database. We need to implement a priority algorithm to manage these situations.',
                        token=token, self=self)
        # Append the concept in the database
        if self.qualified_key not in Concept._concept_database:
            Concept._concept_database[self.qualified_key] = self
        else:
            log.error(
                'The initialization of the concept could not be completed because the qualified key was already present in the static database.',
                qualified_key=self.qualified_key, self=self)

    def __str__(self):
        return self._utf8

    @property
    def arity(self):
        return self._arity

    @property
    def base_key(self):
        return self._base_key

    @staticmethod
    def get_concept_from_decomposed_key(scope_key: str, structure_key: str, language_key: str, base_key: str, **kwargs):
        if scope_key is not None and structure_key is not None and language_key is not None and base_key is not None:
            qualified_key = get_qualified_key(scope_key, structure_key, language_key, base_key)
            return Concept.get_concept_from_qualified_key(
                qualified_key, scope=scope_key, ntype=structure_key, language=language_key, nkey=base_key,
                **kwargs)
        else:
            log.error('Some identification properties are None', scope=scope_key, ntype=structure_key,
                      language=language_key, nkey=base_key, **kwargs)

    @staticmethod
    def get_concept_from_qualified_key(qualified_key, **kwargs):
        if qualified_key is not None:
            if qualified_key in Concept._concept_database:
                return Concept._concept_database[qualified_key]
            else:
                return Concept(qualified_key=qualified_key, **kwargs)
        else:
            log.error('Getting concept with None qualified key is impossible.',
                      qualified_key=qualified_key, **kwargs)

    @staticmethod
    def get_concept_from_token(token):
        """

        Definition:
        A **token** is a list of text symbols that is mapped to a specific concept.
        """
        # TODO: Resume implementation here.
        #   - In Concept __init__: subscribe tokens to a global index and check for unicity.
        pass

    def is_equal_concept(self, other: Concept):
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
            rformat = rformats.DEFAULT
        # TODO: Check that rformat is an allowed value.
        if hasattr(self, rformat):
            return getattr(self, rformat)
        elif self._utf8 is not None:
            # We fall back on UTF-8
            return self._utf8
        else:
            log.error(f'This concept has no representation in {rformat} nor {rformats.UTF8}.', rformat=rformat,
                      qualified_key=self.qualified_key)

    @property
    def structure_key(self) -> str:
        return self._structure_key

    @property
    def python_value(self):
        return self._python_value

    @property
    def qualified_key(self):
        return get_qualified_key(scope=self.scope_key, ntype=self.structure_key, language=self.language,
                                 nkey=self.base_key)

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
        # ...

        # Call the base class initializer.
        #   Executing this at the end of the initialization process
        #   assures that the new concept is not appended to the
        #   static concept and token databases before it is fully initialized.
        super().__init__(
            scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
            utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
            **kwargs)


def set_default_scope(scope_key):
    """Set the default current context."""
    global _DEFAULT_SCOPE_KEY
    # TODO: Allow the usage of friendly name, notes or documentation, etc.
    if scope_key is None:
        log.error(
            f'None is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    if not isinstance(scope_key, str):
        log.error(
            f'The object "{scope_key}" of type "{type(scope_key)}" is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')
    scope_key_cleaned = clean_mnemonic_key(scope_key)
    if scope_key_cleaned != scope_key:
        log.warning(
            f'Please note that the context key "{scope_key}" contained unsupported characters. The allowed characters for context keys are: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}". It was automatically cleaned from unsupported characters. The resulting context key is: {scope_key_cleaned}')
    if scope_key == '':
        log.error(
            f'An empty string is not a valid context key. Please provide a non-empty string composed of the allowed characters: "{_MNEMONIC_KEY_ALLOWED_CHARACTERS}".')

    prefixed_key = _USER_DEFINED_KEY_PREFIX + scope_key_cleaned
    _DEFAULT_SCOPE_KEY = prefixed_key
    log.info(f'Default scope: {scope_key_cleaned}')


def get_default_scope():
    return _DEFAULT_SCOPE_KEY[len(_USER_DEFINED_KEY_PREFIX):]


class Variable(Concept):
    """

    Definition:
    ...
    """

    def __init__(
            self,
            # Identification properties
            scope_key, structure_key, language_key, base_key,
            # Mandatory complementary properties
            domain_key,
            # Conditional complementary properties
            # Representation properties
            utf8=None, latex=None, html=None, usascii=None, tokens=None,
            **kwargs):
        # ...
        self._domain_key = domain_key

        # Call the base class initializer.
        #   Executing this at the end of the initialization process
        #   assures that the new concept is not appended to the
        #   static concept and token databases before it is fully initialized.
        super().__init__(
            scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
            utf8=utf8, latex=latex, html=html, usascii=usascii, tokens=tokens,
            **kwargs)

    def represent_declaration(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        match rformat:
            case rformats.UTF8:
                return f'With {self.represent(rformat)} ∈ {self._domain_key}.'
            case _:
                raise NotImplementedError('TODO')


def declare_variable(domain, base_name=None, index=None):
    # TODO: Provide support for different math fonts (e.g.: https://www.overleaf.com/learn/latex/Mathematical_fonts)
    # TODO: Provide support for indexed variables. Variable declaration should be made with indexes bounds and not individual index values.
    scope_key = _DEFAULT_SCOPE_KEY
    # TODO: Implemented base_name cleaning.
    # base_name = clean_variable_base_name(base_name)
    # TODO: Provide support for both domain argument as domain object or domain key.
    base_key = base_name
    domain_key = None
    if isinstance(domain, Domain):
        domain_key = domain
    elif isinstance(domain, str):
        domain_key = domain
    else:
        log.error('Unsupported domain', domain=domain)
    utf8 = base_name
    latex = base_name
    html = base_name
    usascii = base_name
    v = Variable(
        scope_key=scope_key, structure_key=_STRUCTURE_VARIABLE, language_key=_LANGUAGE_NAIVE, base_key=base_name,
        domain_key = domain_key,
        utf8=utf8, latex=latex, html=html, usascii=usascii)
    log.info(v.represent_declaration())
    return v

def v(domain, base_name = None, index = None):
    """Shorthand function to declare a new variable."""
    declare_variable(domain, base_name, index)


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

    # Constants
    ATOMIC_VARIABLE = 'formula_atomic_variable'  # TODO: Question: is it justified to distinguish this from FORMULA_VARIABLE?
    FORMULA_VARIABLE = 'formula_formula_variable'  # TODO: Question: is it justified to distinguish this from ATOMIC_VARIABLE?
    SYSTEM_CONSTANT_CALL = 'formula_constant_call'  # Aka a 0-ary function.
    SYSTEM_UNARY_OPERATOR_CALL = 'formula_unary_operator_call'
    SYSTEM_BINARY_OPERATOR_CALL = 'formula_binary_operator_call'
    SYSTEM_N_ARY_FUNCTION_CALL = 'formula_n_ary_function_call'
    CATEGORIES = [ATOMIC_VARIABLE, FORMULA_VARIABLE, SYSTEM_CONSTANT_CALL, SYSTEM_UNARY_OPERATOR_CALL, SYSTEM_BINARY_OPERATOR_CALL,
                  SYSTEM_N_ARY_FUNCTION_CALL]

    def __init__(
            self,
            # Identification properties
            scope_key, structure_key, language_key, base_key,
            # Mandatory complementary properties
            category,
            # Conditional complementary properties
            system_function,
            arguments,
            **kwargs):
        # Mandatory complementary properties.
        if category not in Formula.CATEGORIES:
            log.error('Invalid formula category',
                      category=category, qualified_key=self.qualified_key)
        self._category = category
        self._system_function = system_function
        self._arguments = arguments

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
    def category(self):
        return self._category

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # if self.category == Formula.ATOMIC_VARIABLE:
        #     return self.symbol.represent(rformat, *args, **kwargs)
        match self.category:
            case Formula.SYSTEM_CONSTANT_CALL:
                # x
                return f'{self._system_function.represent(rformat)}'
            case Formula.SYSTEM_UNARY_OPERATOR_CALL:
                # fx
                return f'{self._system_function.represent(rformat)}{self.arguments[0].represent(rformat)}'
            case Formula.SYSTEM_BINARY_OPERATOR_CALL:
                # x f y
                return f'{glyphs.parenthesis_left.represent(rformat)}{self.arguments[0].represent(rformat)}{glyphs.small_space.represent(rformat)}{self._system_function.represent(rformat)}{glyphs.small_space.represent(rformat)}{self.arguments[1].represent(rformat)}{glyphs.parenthesis_right.represent(rformat)}'
            case Formula.SYSTEM_N_ARY_FUNCTION_CALL:
                # f(x,y,z)
                variable_list = ', '.join(map(lambda a: a.represent(), self.arguments))
                return f'{self._system_function.represent(rformat)}{glyphs.parenthesis_left.represent(rformat)}{variable_list}{glyphs.parenthesis_right.represent(rformat)}'
            case _:
                log.error('Unsupported formula category', category=self.category, qualified_key=self.qualified_key)

    @property
    def system_function(self):
        return self._system_function


class Counter(object):
    def __init__(self):
        self.value = 1
        self._lock = threading.Lock()

    def get_value(self):
        with self._lock:
            self.value += 1
            return self.value

_FORMULA_AUTO_COUNTER = Counter()

def write_formula(o, *args):
    global _FORMULA_AUTO_COUNTER
    scope_key = _DEFAULT_SCOPE_KEY
    index = _FORMULA_AUTO_COUNTER.get_value()
    base_key = 'f' + str(index)
    category = None
    system_function = None
    if isinstance(o, SystemFunction):
        system_function = o
        match o.category:
            case SystemFunction.SYSTEM_CONSTANT:
                category = Formula.SYSTEM_CONSTANT_CALL
            case SystemFunction.SYSTEM_UNARY_OPERATOR:
                category = Formula.SYSTEM_UNARY_OPERATOR_CALL
            case SystemFunction.SYSTEM_BINARY_OPERATOR:
                category = Formula.SYSTEM_BINARY_OPERATOR_CALL
            # TODO: Implement all other possibilities
    arguments = args
    formula = Formula(
        # Identification properties
        scope_key=scope_key, structure_key=_STRUCTURE_FORMULA, language_key=_LANGUAGE_NAIVE, base_key=base_key,
        # Mandatory complementary properties
        category=category,
        # Conditional complementary properties
        system_function=system_function, arguments=arguments
    )
    log.info(formula.represent())
    return formula


def f(o, *args):
    """Shorthand function to write a formula."""
    return write_formula(o, *args)


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
            codomain, category,
            # Conditional complementary properties
            domain=None, arity=None, python_value=None,
            # Representation properties
            utf8=None, latex=None, html=None, usascii=None, tokens=None,
            **kwargs):
        # Mandatory complementary properties.
        self._codomain = codomain  # TODO: Implement validation against the static concept database.
        if category not in SystemFunction.CATEGORIES:
            log.error('Invalid formula category',
                      category=category, qualified_key=self.qualified_key)
        self._category = category
        # Conditional complementary properties.
        self._domain = domain  # TODO: Implement validation against the static concept database.
        self._arity = arity  # TODO: Implement validation logic dependent of subcategory.
        if category == SystemFunction.SYSTEM_CONSTANT and python_value is None:
            log.error('python_value is mandatory for constants (0-ary functions) but it was None.',
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
        if self.category == SystemFunction.SYSTEM_CONSTANT:
            return self._python_value
        else:
            raise NotImplementedError('ooops')

    def equal_programmatic_value(self, other):
        """Return true if two formula yield identical values, false otherwise."""
        if isinstance(other, Formula) and other.subcategory == SystemFunction.SYSTEM_CONSTANT:
            return self.compute_programmatic_value() == other.compute_programmatic_value()
        else:
            raise NotImplementedError('oooops again')


def get_qualified_key(scope, ntype, language, nkey):
    return f'{scope}{_QUALIFIED_KEY_SEPARATOR}{ntype}{_QUALIFIED_KEY_SEPARATOR}{language}{_QUALIFIED_KEY_SEPARATOR}{nkey}'


# Scope.
system_scope = Scope(
    scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE, base_key='sys',
    utf8='sys', latex=r'\text{sys}', html='sys', usascii='sys')

initial_user_defined_scope = Scope(
    scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE,
    base_key=_USER_DEFINED_KEY_PREFIX + 'scope_1',
    utf8='scope₁', latex=r'\text{scope}_1', html=r'scope<sub>1</sub>', usascii='scope1')
# TODO: Question: what should be the scope_key of user defined scopes? sys? the scope itself?

set_default_scope('scope_1')
