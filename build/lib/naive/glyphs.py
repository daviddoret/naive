from _class_glyph import Glyph

# Number sets
standard_0 = Glyph(utf8='0', latex=r'0', html='0', usascii='0')
standard_1 = Glyph(utf8='1', latex=r'1', html='1', usascii='1')
standard_x_lowercase = Glyph(utf8='v', latex=r'v', html='v', usascii='v')
standard_y_lowercase = Glyph(utf8='y', latex=r'y', html='y', usascii='y')
standard_z_lowercase = Glyph(utf8='z', latex=r'z', html='z', usascii='z')
mathbb_a_uppercase = Glyph(utf8='𝔸', latex=r'\mathbb{A}', html='&Aopf;', usascii='A')
mathbb_b_uppercase = Glyph(utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
mathbb_n_uppercase = Glyph(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', usascii='N')
mathbb_z_uppercase = Glyph(utf8='ℤ', latex=r'\mathbb{Z}', html='&Zopf;', usascii='Z')
# {\displaystyle \mathbb {C} }\mathbb{C} 	ℂ	Complex number	\mathbb{C}, \Complex	&Copf;	U+2102
# {\displaystyle \mathbb {H} }\mathbb {H} 	ℍ	Quaternion	\mathbb{H}, \H	&quaternions;	U+210D
# {\displaystyle \mathbb {O} }\mathbb {O} 	𝕆	Octonion	\mathbb{O}	&Oopf;	U+1D546
# {\displaystyle \mathbb {Q} }\mathbb {Q} 	ℚ	Rational number	\mathbb{Q}, \Q	&Qopf;	U+211A
# {\displaystyle \mathbb {R} }\mathbb {R} 	ℝ	Real number	\mathbb{R}, \R	&Ropf;	U+211D
# {\displaystyle \mathbb {S} }\mathbb {S} 	𝕊	Sedenion	\mathbb{S}	&Sopf;	U+1D54A

to = Glyph(utf8='⟶', latex=r'\longrightarrow', html=r'&rarr;', usascii='-->')
maps_to = Glyph(utf8='⟼', latex=r'\longmapsto', html=r'&mapsto;', usascii='|->')
colon = Glyph(utf8=':', latex=r'\colon', html=r':', usascii=':')

# Bibliography:
#   * https://en.wikipedia.org/wiki/List_of_logic_symbols
logical_falsum = Glyph(utf8='⊥', latex=r'\bot', html='&perp;', usascii='F')
logical_truth = Glyph(utf8='⊤', latex=r'\top', html='&top;', usascii='T')
logical_negation = Glyph(utf8='¬', latex=r'\lnot', html='&not;', usascii='not')
logical_conjunction = Glyph(utf8='∧', latex=r'\land', html='&and;', usascii='and')
logical_disjunction = Glyph(utf8='∨', latex=r'\lor', html='&or;', usascii='or')
logical_material_implication = Glyph(utf8='⇒', latex=r'\implies', html='&rArr;', usascii='implies')
logical_material_equivalence = Glyph(utf8='⇔', latex=r'\iif', html='&hArr;', usascii='iif')


# Greek Letters
phi_plain_small = Glyph(utf8='φ', latex=r'\phi', html='&phi;', usascii='phi')
phi_plain_cap = Glyph(utf8='Φ', latex=r'\Phi', html='&Phi;', usascii='Phi')
psi_plain_small = Glyph(utf8='ψ', latex=r'\psi', html='&psi;', usascii='psi')
psi_plain_cap = Glyph(utf8='Ψ', latex=r'\Psi', html='&Psi;', usascii='Psi')

# Brackets
# Sources:
#   * https://en.wikipedia.org/wiki/Bracket
parenthesis_left = Glyph(utf8='(', latex=r'\left(', html='&lparen;', usascii='(')
parenthesis_right = Glyph(utf8=')', latex=r'\right)', html='&rparen;', usascii=')')
square_bracket_left = Glyph(utf8='[', latex=r'\left[', html='&91;', usascii='[')
square_bracket_right = Glyph(utf8=']', latex=r'\right]', html='&93;', usascii=']')
curly_bracket_left = Glyph(utf8='{', latex=r'\left\{', html='&123;', usascii='{')
curly_bracket_right = Glyph(utf8='}', latex=r'\right\}', html='&125;', usascii='}')
angle_bracket_left = Glyph(utf8='⟨', latex=r'\left\langle', html='&lang;', usascii='<')
angle_bracket_right = Glyph(utf8='⟩', latex=r'\right\rangle', html='&rang;', usascii='>')

# Set Theory
element_of = Glyph(utf8='∈∉', latex=r'\in')
not_element_of = Glyph(utf8='∉', latex=r'\notin')

# Spaces
small_space = Glyph(utf8=' ', latex=r'\,', html='&nbsp;', usascii=' ')