
def clean_math_variable(s: str) -> str:
    """Clean a string from characters that are unusual in math variable names.

    Basically we keep alphanumeric characters, including greek letters, subscripts and superscripts.

    Incidentally, the idea is to avoid ambiguities and confusions that may arise from unwanted characters such as punctuation and mathematical operators.

    :param s: A raw variable name that potentially contains unusual characters.
    :return: A clean variable name that is safe from unusual characters.
    """
    return ''.join([c for c in str(s) if c.isalpha() or c.isdigit()])