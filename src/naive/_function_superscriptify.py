import rformats


def superscriptify(representation: str, rformat: str) -> str:
    """Converts to superscript the representation of object **o**.

    Use cases:
        * Render beautiful indexed math variables (e.g. x₁, x₂, x₃).

    Args:
        representation (str): The representation of the object in that format.
        rformat (str): A supported format from the formats.CATALOG.

    Returns:
        str: The representation in superscript.

    Example:

        .. jupyter-execute::

            # TODO: Rewrite
            #import naive
            #o = 'Indexed math variables look beautiful with superscript: x1, x2, x3'
            #s_prime = naive.superscript(o)
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
        case rformats.LATEX:
            # ASSUMPTION: The superscriptified result must be concatenated with something.
            return r'^{' + representation + r'}'
        case rformats.HTML:
            return r'<sup>' + representation + r'</sup>'
        case rformats.ASCII:
            # TODO: ASCII representation may be ambiguous. Considering issuing a Warning.
            return representation
