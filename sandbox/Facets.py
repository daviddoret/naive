import typing


class Utils:
    def clean_mnemonic_key(mnemonic_key):
        return mnemonic_key


class Facet(str):
    def __init__(self, mnemonic_key: str):
        super().__init__()


class Facets:
    # Declaration of Naive system facets.
    scope = Facet('scope')
    language = Facet('language')
    codomain = Facet('codomain')
    function = Facet('function')
    atomic_property = Facet('ap')
    variable = Facet('variable')
    formula = Facet('formula')
    set = Facet('set')


class FacetedPropertyName(str):
    def __init__(self, facets):
        self._facets = facets


class FacetedPropertyNames:
    arity = FacetedPropertyName([Facets.atomic_property, Facets.formula])
    commutativity = FacetedPropertyName([Facets.formula, Facets.scope])

def get_faceted_property_value(self, property):
    if set(self.facets).intersection(property.facets):
        return getattr(self, '_' + property)
    else:
        print('This object has no facet supporting this property')

class Concept:

    def __init__(self):
        init_faceted_property()

    x = property((lambda self: self), None, None, "I'm the 'x' property.")


c1 = Concept()
print(c1.x)
