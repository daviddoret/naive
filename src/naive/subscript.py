from src.naive.coerce import coerce


def subscript(s: (str, int)) -> str:
    """Converts to subscript digits the digits in a Unicode string `s`.

    This function is especially useful to render beautiful indexed math variables (e.g. x₁, x₂, x₃) with raw text.

    Args:
        s (str): A Unicode `str` that may contain digits.

    Returns:
        str: A Unicode `str` where all digits are replaced with subscript digits.

    Example:

        .. jupyter-execute::

            import naive
            s = 'Indexed math variables look beautiful with subscript: x1, x2, x3'
            s_prime = naive.subscript(s)
            print(s_prime)

    References:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    """
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
    s = coerce(s, str)
    return u''.join(subscript_dictionary.get(char, char) for char in s)