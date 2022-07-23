"""Representation Formats.

Every format is an alphanumeric key that is used as an object attribute with hasattr(),
setattr(), and getattr() to store object representations in the corresponding formats.
"""

# REPRESENTATION FORMAT ENTRIES

"""The USASCII representation format. 

Implemented as standard pythonic strings, but assured to be USASCII-compatible."""
USASCII = 'usascii'

"""The UTF-8 representation format. 

Implemented as standard pythonic strings (as of Python 3.0 and above), encoded in the default UTF-8. """
UTF8 = 'utf8'

"""The LaTeX representation format.

Implemented as UTF-8 standard strings with LaTeX encoding.
"""
LATEX = 'latex'

"""The HTML representation format.

Implemented as UTF-8 standard strings with HTML character encoding.
"""
HTML = 'html'

# DEFAULT REPRESENTATION FORMAT

"""The default representation format.

All representations are rendered in the default format, unless specified otherwise."""
DEFAULT = UTF8  # You may change this.

# LIST OF REPRESENTATION FORMATS

"""The list of all available formats."""
CATALOG = [USASCII, UTF8, LATEX, HTML]
