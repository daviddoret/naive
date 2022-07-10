import glyphs
from _class_domain import Domain

"""The binary or boolean domain."""
b = Domain(glyphs.mathbb_b_uppercase)

"""The natural numbers domain, 0 inclusive"""
n0 = Domain(glyphs.mathbb_n_uppercase, 0)

"""The natural numbers domain, 0 exclusive"""
n1 = Domain(glyphs.mathbb_n_uppercase, 1)

"""The integer numbers domain"""
z = Domain(glyphs.mathbb_z_uppercase)

