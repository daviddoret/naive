import rformats


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
            #s_prime = naive.subscript(o)
            #print(s_prime)

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    """
    if representation is None:
        return ''
    if rformat is None:
        rformat = rformats.DEFAULT
    match rformat:
        case rformats.UTF8:
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
        case rformats.LATEX:
            # ASSUMPTION: The subscriptified result must be concatenated with something.
            return r'_{' + representation + r'}'
        case rformats.HTML:
            return r'<sub>' + representation + r'</sub>'
        case rformats.ASCII:
            # TODO: ASCII representation may be ambiguous. Considering issuing a Warning.
            return representation
