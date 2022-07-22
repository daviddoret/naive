from __future__ import annotations
import log


# Concept Core Properties
import rformats

_BASE_KEY = 'base_key'
_STRUCTURE_KEY = 'structure_key'
_SCOPE_KEY = 'scope_key'
_LANGUAGE_KEY = 'language_key'

# Function Complementary Properties
_DOMAIN = 'domain'
_CODOMAIN = 'codomain'
_ARITY = 'arity'
_PYTHON_VALUE = 'python_value'

# NType Keys
_STRUCTURE_LANGUAGE = 'language_key'
_STRUCTURE_DOMAIN = 'domain'
_STRUCTURE_FUNCTION = 'function'
_STRUCTURE_ATOMIC_PROPERTY = 'ap'

_QUALIFIED_KEY_SEPARATOR = '.'
_MNEMONIC_KEY_ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz012345679'


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
                    log.error(f'The "{token}" token was already in the token static database. We need to implement a priority algorithm to manage these situations.', token=token, self=self)
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
            log.error('Some identification properties are None', scope=scope_key, ntype=structure_key, language=language_key, nkey=base_key, **kwargs)

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
            log.error(f'This concept has no representation in {rformat} nor {rformats.UTF8}.', rformat=rformat, qualified_key=self.qualified_key)

    @property
    def structure_key(self) -> str:
        return self._structure_key

    @property
    def python_value(self):
        return self._python_value

    @property
    def qualified_key(self):
        return get_qualified_key(scope=self.scope_key, ntype=self.structure_key, language=self.language, nkey=self.base_key)

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

# Formula categories
VARIABLE = 'variable'
FUNCTION = 'function call'
FORMULA_CATEGORIES = [VARIABLE, FUNCTION]

# Formula subcategories
ATOMIC_VARIABLE = 'atomic'
FORMULA_VARIABLE = 'formula'
CONSTANT = 'constant call'
UNARY_OPERATOR = 'unary operator call'
BINARY_OPERATOR = 'binary operator call'
N_ARY_FUNCTION = 'n-ary function call'
FORMULA_SUBCATEGORIES = {
    VARIABLE: [ATOMIC_VARIABLE, FORMULA_VARIABLE],
    FUNCTION: [CONSTANT, UNARY_OPERATOR, BINARY_OPERATOR, N_ARY_FUNCTION]}


class Formula(Concept):
    """

    Different types of formula:
    - Atomic Variable (aka Unknown) (e.g. x + 5 = 17, x ∉ ℕ₀)
    - Formula Variable (e.g. φ = ¬x ∨ y, z ∧ φ)
    - n-ary Function Call with n in N0 (e.g. za1 abs)

    Different sub-types of n-ary Functions:
    - 0-ary Operator (aka Constant) (e.g. ba1 truth)
    - Unary Operator (e.g. ba1 negation)
    - Binary Operator (e.g. ba1 conjunction)
    - n-ary Function

    """
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


class Function(Concept):

    def __init__(
            self,
            # Identification properties
            scope_key, structure_key, language_key, base_key,
            # Mandatory complementary properties
            codomain, category, subcategory,
            # Conditional complementary properties
            domain=None, arity=None, python_value=None,
            # Representation properties
            utf8=None, latex=None, html=None, usascii=None, tokens=None,
            **kwargs):
        # Mandatory complementary properties.
        self._codomain = codomain  # TODO: Implement validation against the static concept database.
        if category not in FORMULA_CATEGORIES:
            log.error('Invalid formula category',
                      category=category, self=self)
        self._category = category  # TODO: Implement validation against allowed values.
        if subcategory not in FORMULA_SUBCATEGORIES[category]:
            log.error('Invalid formula subcategory',
                      subcategory=subcategory, category=category, self=self)
        self._subcategory = subcategory  # TODO: Implement validation logic dependent of category.
        # Conditional complementary properties.
        self._domain = domain  # TODO: Implement validation against the static concept database.
        self._arity = arity  # TODO: Implement validation logic dependent of subcategory.
        if subcategory == CONSTANT and python_value is None:
            log.error('python_value is mandatory for constants (0-ary functions) but it was None.',
                      python_value=python_value, subcategory=subcategory, self=self)
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
    def codomain(self):
        return self._codomain

    @property
    def domain(self):
        return self._domain

    @property
    def compute_value(self):
        if self._subcategory == CONSTANT:
            return self._python_value
        else:
            raise NotImplementedError('ooops')

    def is_equal_value(self, other):
        """Return true if two formula yield identical values, false otherwise."""
        if isinstance(other, Formula) and other.subcategory == CONSTANT:
            return self.compute_value() == other.compute_value()
        else:
            raise NotImplementedError('oooops again')


def get_qualified_key(scope, ntype, language, nkey):
    return f'{scope}{_QUALIFIED_KEY_SEPARATOR}{ntype}{_QUALIFIED_KEY_SEPARATOR}{language}{_QUALIFIED_KEY_SEPARATOR}{nkey}'


def instantiate_concept(**kwargs):
    # TODO: This is just an idea. It would be easy to develop
    #  a transversal factory function that would call the correct
    #  constructor based on the structure_key argument.
    pass


# Friendly programmatic writing functions

def f():
    """Instanciates a function formula element."""
    pass

def v():
    """Instanciates an atomic variable formula element."""
    pass

def c():
    """Instanciates a constant formula element."""
    pass
