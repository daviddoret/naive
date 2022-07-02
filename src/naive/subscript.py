def subscript(s):
    """


    Bibliography:
        * https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript

    :param s:
    :return:
    """
    subscript_dictionary = {'0': '₀',
                            '1': '₁',
                            '2': '₂',
                            '3': '₃',
                            '4': '₄',
                            '5': '₅',
                            '6': '₆',
                            '7': '₇',
                            '8': '₈',
                            '9': '₉'}
    return ''.join(subscript_dictionary.get(char, char) for char in s)