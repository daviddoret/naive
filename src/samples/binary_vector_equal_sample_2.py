"""Binary Vector Equality Operator - Code Sample 2

This code sample illustrates how the equality operator behaves on a small sample of distinctive binary vectors"""
import src.naive.type_library as tl

v1 = tl.BV([])  # This is equivalent to the empty set
v2 = tl.BV([0])
v3 = tl.BV([1, 0])
v4 = tl.BV([1, 0, 1])
v5 = tl.BV(None)  # This is equivalent to undefined
v_sample = [v1, v2, v3, v4, v5]  # Bundle all our vectors
# Apply the = operator to all combinations of vectors
for v in v_sample:
    for w in v_sample:
        print(f'( {v} = {w} ) = {v == w}')

