from __future__ import annotations
from collections.abc import Iterable
import log
from _function_subscriptify import subscriptify
from _function_superscriptify import superscriptify
import threading
from _function_represent import represent

# Concept Core Properties
import rformats
import glyphs

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
_STRUCTURE_FORMULA = 'phi'

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
                qualified_key=self.qualified_key)

    def __str__(self):
        return self.represent(rformats.UTF8)

    def __repr__(self):
        return self.represent(rformats.UTF8)

    @property
    def arity(self):
        return self._arity

    @property
    def base_key(self):
        return self._base_key

    @staticmethod
    def check_concept_from_decomposed_key(scope_key: str, structure_key: str, language_key: str, base_key: str, **kwargs):
        if scope_key is not None and structure_key is not None and language_key is not None and base_key is not None:
            qualified_key = get_qualified_key(scope_key, structure_key, language_key, base_key)
            return Concept.check_concept_from_qualified_key(
                qualified_key, scope=scope_key, ntype=structure_key, language=language_key, nkey=base_key,
                **kwargs)
        else:
            log.error('Some identification properties are None', scope=scope_key, ntype=structure_key,
                      language=language_key, nkey=base_key, **kwargs)

    @staticmethod
    def check_concept_from_qualified_key(qualified_key, **kwargs):
        if qualified_key is not None:
            return qualified_key in Concept._concept_database
        else:
            log.error('Checking concept with None qualified key is impossible.',
                      qualified_key=qualified_key, **kwargs)

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
        #   - In Concept __init__: subscribe tokens to a global indexes and check for unicity.
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
        return get_qualified_key(scope_key=self.scope_key, structure_key=self.structure_key, language_key=self.language,
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
    log.info(f'Default scope_key: {scope_key_cleaned}')


def get_default_scope():
    return _DEFAULT_SCOPE_KEY[len(_USER_DEFINED_KEY_PREFIX):]


def declare_variable(codomain, base_name=None, indexes=None):
    # TODO: Provide support for different math fonts (e.g.: https://www.overleaf.com/learn/latex/Mathematical_fonts)
    # TODO: Provide support for indexed variables. Variable declaration should be made with indexes bounds and not individual indexes values.
    codomain_key = None
    # Identification properties
    scope_key = _DEFAULT_SCOPE_KEY
    structure_key = _STRUCTURE_FORMULA
    language_key = _LANGUAGE_NAIVE
    if base_name is None:
        # TODO: Make this a scope preference setting, letting the user choose the default
        #   variable base_name in that scope.
        base_name = 'x'
    base_key = base_name
    if indexes is not None:
        if not isinstance(indexes, Iterable):
            base_key = base_key + '__' + str(indexes)
        else:
            base_key = base_key + '__' + '_'.join(str(index) for index in indexes)
    if Concept.check_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key):
        variable = Concept.get_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key)
        log.warning('This variable is already declared. In consequence, the existing variable is returned, instead of declaring a new one.', variable=variable, scope_key=scope_key)
        return variable
    else:
        variable = Formula(
            scope_key=scope_key, language_key=language_key, base_key=base_key,
            category=Formula.ATOMIC_VARIABLE,
            codomain= codomain, base_name=base_name, indexes=indexes)
        log.info(variable.represent_declaration())
        return variable


def v(codomain, base_name = None, indexes = None):
    """Shorthand function to declare a new variable."""
    return declare_variable(codomain, base_name, indexes)


class Formula(Concept):
    """

    Definition:
    A phi, in the context of the naive package,
    is a tree of "calls" to functions, constants, or variables.
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
    # TODO: Issue a warning when a property is accessed when the category make it invalid.

    # Constants
    ATOMIC_VARIABLE = 'formula_atomic_variable'  # TODO: Question: is it justified to distinguish this from FORMULA_VARIABLE?
    FORMULA_VARIABLE = 'formula_formula_variable'  # TODO: Question: is it justified to distinguish this from atomic_variable?
    SYSTEM_CONSTANT_CALL = 'programmatic_constant_call'  # Aka a 0-ary function.
    SYSTEM_UNARY_OPERATOR_CALL = 'programmatic_unary_operator_call'
    SYSTEM_BINARY_OPERATOR_CALL = 'programmatic_binary_operator_call'
    SYSTEM_N_ARY_FUNCTION_CALL = 'programmatic_n_ary_function_call'
    CATEGORIES = [ATOMIC_VARIABLE, FORMULA_VARIABLE, SYSTEM_CONSTANT_CALL, SYSTEM_UNARY_OPERATOR_CALL, SYSTEM_BINARY_OPERATOR_CALL,
                  SYSTEM_N_ARY_FUNCTION_CALL]

    def __init__(
            self,
            # Identification properties
            scope_key, language_key, base_key,
            # Mandatory complementary properties
            category,
            # Conditional complementary properties
            # ...for system function calls:
            system_function = None, arguments = None,
            # ...for atomic variables
            domain = None, codomain = None, base_name = None, indexes = None,
            **kwargs):
        # Identification properties
        structure_key = _STRUCTURE_FORMULA
        # Mandatory complementary properties.
        if category not in Formula.CATEGORIES:
            log.error('Invalid phi category',
                      category=category, qualified_key=self.qualified_key)
        self._category = category
        self._arity = None
        self._system_function = system_function
        # match category:
        #     case Formula.atomic_variable:
        #         # The rationale for this arity = 0 is that atomic variables have no input.
        #         # This would be wrong of phi variables.
        #         self._arity = 0
        #     case Formula.programmatic_constant_call:
        #         self._arity = 0
        #     case Formula.programmatic_unary_operator_call:
        #         self._arity = 1
        #     case Formula.programmatic_binary_operator_call:
        #         self._arity = 2
        #     # Replace the match ... case ... with system.function.arity.
        #     # TODO: Implement arity for n-ary system function calls.
        #     # TODO: Implement arity for phi variables.
        #     # TODO: Consider making this property a dynamic property.
        self._arguments = arguments
        self._domain = 'NOT IMPLEMENTED'  # TODO: Implement phi domain. It may be None, a base domain or a tuple of domains.
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
        if self.category == Formula.ATOMIC_VARIABLE:
            # For atomic variables, the arity is 0.
            # The rationale is that an atomic variable doesn't get any input.
            # This would be wrong of phi variables which deserver a distinct implementation.
            return 0
        elif self.is_system_function_call:
            # For system function calls, the arity of the call
            # is equal to the arity of the function being called.
            return self.system_function.arity
        else:
            # TODO: Implement the arity property for all object categories.
            log.warning('The arity property has not been implemented for this concept category.', category=self.category, self=self)

    @property
    def category(self):
        return self._category

    @property
    def codomain(self):
        if self.category == Formula.ATOMIC_VARIABLE:
            # For atomic variables, the codomain is part of the object.
            return self._codomain
        elif self.is_system_function_call:
            # For system function calls, the codomain of the function call
            # is equal to the codomain of the function being called.
            return self.system_function.codomain
        else:
            # TODO: Implement the codomain property for all object categories.
            log.warning('The codomain property has not been implemented for this concept category.', category=self.category, self=self)

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

        If *True*, the instance has the *programmatic_function* property.
        """
        return self.category in [
            Formula.SYSTEM_CONSTANT_CALL,
            Formula.SYSTEM_UNARY_OPERATOR_CALL,
            Formula.SYSTEM_BINARY_OPERATOR_CALL,
            Formula.SYSTEM_N_ARY_FUNCTION_CALL]

    def list_atomic_variables(self):
        """Return the sorted set of variables present in the phi, and its subformulae recursively."""
        l = set()
        for a in self.arguments:
            if isinstance(a, Formula) and a.category == Formula.ATOMIC_VARIABLE:
                l.add(a)
            elif isinstance(a, Formula):
                l_prime = a.list_atomic_variables()
                for a_prime in l_prime:
                    l.add(a_prime)
            else:
                log.error('Not implemented yet', a=a, self=self)

        # To allow sorting and indexing, convert the set to a list.
        l = list(l)
        l.sort(key=lambda x: x.base_key)
        return l

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # if self.category == Formula.atomic_variable:
        #     return self.symbol.represent(rformat, *args, **kwargs)
        match self.category:
            case Formula.ATOMIC_VARIABLE:
                # x
                # TODO: Modify approach. Storing and returning the _base_name like this
                #   prevent support for other mathematical fonts, such as MathCal, etc.
                #   As an initial approach, it provides support for ASCII like variables.
                #   We may consider storing a Glyph as the base name,
                #   and calling the static represent() function.
                return self._base_name + \
                       subscriptify(represent(self._indexes, rformat), rformat)
            case Formula.SYSTEM_CONSTANT_CALL:
                # x
                return f'{self._system_function.represent(rformat)}'
            case Formula.SYSTEM_UNARY_OPERATOR_CALL:
                # fx
                return f'{self._system_function.represent(rformat)}{self.arguments[0].represent(rformat)}'
            case Formula.SYSTEM_BINARY_OPERATOR_CALL:
                # (x f y)
                return f'{glyphs.parenthesis_left.represent(rformat)}{self.arguments[0].represent(rformat)}{glyphs.small_space.represent(rformat)}{self._system_function.represent(rformat)}{glyphs.small_space.represent(rformat)}{self.arguments[1].represent(rformat)}{glyphs.parenthesis_right.represent(rformat)}'
            case Formula.SYSTEM_N_ARY_FUNCTION_CALL:
                # f(x,y,z)
                variable_list = ', '.join(map(lambda a: a.represent(), self.arguments))
                return f'{self._system_function.represent(rformat)}{glyphs.parenthesis_left.represent(rformat)}{variable_list}{glyphs.parenthesis_right.represent(rformat)}'
            case _:
                log.error('Unsupported phi category', category=self.category, qualified_key=self.qualified_key)

    def represent_declaration(self, rformat: str = None, *args, **kwargs) -> str:
        if self.category != Formula.ATOMIC_VARIABLE:
            log.error('Formula category not supported for declaration.')
        else:
            if rformat is None:
                rformat = rformats.DEFAULT
            match rformat:
                case rformats.UTF8:
                    return f'With {self.represent(rformat)} ∈ {self.codomain.represent(rformat)}.'
                case _:
                    raise NotImplementedError('TODO')

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
        scope_key=scope_key, language_key=_LANGUAGE_NAIVE, base_key=base_key,
        # Mandatory complementary properties
        category=category,
        # Conditional complementary properties
        system_function=system_function, arguments=arguments
    )
    log.info(formula.represent())
    return formula


def f(o, *args):
    """Shorthand function to write a phi."""
    return write_formula(o, *args)


class SystemFunction(Concept):
    """The system function class.

    Definition:
    A system function, in the context of the naive package,
    is a function that is predefined in the sense that it is accompanied by a programmatic algorithm and not a phi,
    and atomic in the sense that it cannot be further decomposed into constituent sub-formulae.

    """

    # Constants
    SYSTEM_CONSTANT = 'programmatic_constant'  # Aka a 0-ary function.
    SYSTEM_UNARY_OPERATOR = 'programmatic_unary_operator'  # Aka a unary function with operator notation.
    SYSTEM_BINARY_OPERATOR = 'programmatic_binary_operator'  # Aka a binary function with operator notation.
    SYSTEM_N_ARY_FUNCTION = 'programmatic_n_ary_function'
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
        if category not in SystemFunction.CATEGORIES:
            log.error('Invalid phi category',
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
        if self.category == SystemFunction.SYSTEM_CONSTANT:
            return self._python_value
        else:
            raise NotImplementedError('ooops')

    def equal_programmatic_value(self, other):
        """Return true if two phi yield identical values, false otherwise."""
        if isinstance(other, Formula) and other.subcategory == SystemFunction.SYSTEM_CONSTANT:
            return self.compute_programmatic_value() == other.compute_programmatic_value()
        else:
            raise NotImplementedError('oooops again')


def get_qualified_key(scope_key, structure_key, language_key, base_key):
    return f'{scope_key}{_QUALIFIED_KEY_SEPARATOR}{structure_key}{_QUALIFIED_KEY_SEPARATOR}{language_key}{_QUALIFIED_KEY_SEPARATOR}{base_key}'


# Scope.
system_scope = Scope(
    scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE, base_key='sys',
    utf8='sys', latex=r'\text{sys}', html='sys', usascii='sys')

initial_user_defined_scope = Scope(
    scope_key='sys', structure_key=_STRUCTURE_SCOPE, language_key=_LANGUAGE_NAIVE,
    base_key=_USER_DEFINED_KEY_PREFIX + 'scope_1',
    utf8='scope_key₁', latex=r'\text{scope_key}_1', html=r'scope_key<sub>1</sub>', usascii='scope1')
# TODO: Question: what should be the scope_key of user defined scopes? sys? the scope_key itself?

set_default_scope('scope_1')
