
def clean_math_symbol(s: str) -> str:
    """Clean a string from characters that are unusual in math symbols.

    Basically we keep alphanumeric characters, including greek letters,
    subscripts and superscripts.

    The objective of this function is to avoid ambiguities and confusions,
    which may arise from undesirable characters such as spaces and hidden characters.

    Args:
        s (str): A raw string that potentially contains undesirable characters.

    Returns:
        str: A clean variable name, safe from undesirable characters.

    """
    return ''.join([c for c in str(s) if c.isalpha() or c.isdigit()])