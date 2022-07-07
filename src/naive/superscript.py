from src.naive import coerce


def superscript(s: str) -> str:
    """

    Bibliography:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    Args:
        :param s:
        :return:
    """
    s = coerce(s, str)
    subscript_dictionary = {'0': '⁰',
                            '1': '¹',
                            '2': '²',
                            '3': '³',
                            '4': '⁴',
                            '5': '⁵',
                            '6': '⁶',
                            '7': '⁷',
                            '8': '⁸',
                            '9': '⁹'}
    return ''.join(subscript_dictionary.get(char, char) for char in s)
