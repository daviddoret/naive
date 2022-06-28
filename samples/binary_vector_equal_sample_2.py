"""Binary Vector Equality Operator - Code Sample 2

This code sample illustrates how the equality operator behaves on a small sample of distinctive binary vectors"""
import naive.binary_algebra as ba

v1 = []  # This is equivalent to the empty set
v2 = [0]
v3 = [1, 0]
v4 = [1, 0, 1]
v5 = None  # This is equivalent to undefined
v_sample = [v1, v2, v3, v4, v5]  # Bundle all our vectors
# Apply the = operator to all combinations of vectors
for v in v_sample:
    for w in v_sample:
        print(f'( {v} = {w} ) = {ba.binary_vector_equal(v, w)}')

