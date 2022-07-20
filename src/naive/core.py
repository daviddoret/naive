from __future__ import annotations
import log


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
    pass

class Domain(Concept):
    pass

class Function(Concept):

    def __init__(
            self,
            scope_key, structure_key, language_key, base_key,
            codomain,
            utf8=None, latex=None, html=None, usascii=None, tokens=None,
            domain=None, arity=None, pythong_value=None,
            **kwargs):
        # Complementary Properties.
        self._codomain = codomain
        self._domain = domain
        self._arity = arity
        self._python_value = pythong_value
        # Call the base class initializer.
        super().__init__(
            scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
            utf8=None, latex=None, html=None, usascii=None, tokens=None,
            **kwargs)

    @property
    def codomain(self):
        return self._codomain

    @property
    def domain(self):
        return self._domain


def get_qualified_key(scope, ntype, language, nkey):
    return f'{scope}{_QUALIFIED_KEY_SEPARATOR}{ntype}{_QUALIFIED_KEY_SEPARATOR}{language}{_QUALIFIED_KEY_SEPARATOR}{nkey}'


def instantiate_concept(**kwargs):
    # TODO: This is just an idea. It would be easy to develop
    #  a transversal factory function that would call the correct
    #  constructor based on the structure_key argument.
    pass


# Concept Core Properties
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
