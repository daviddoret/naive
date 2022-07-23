"""Binary Vector Equality Operator - Code Sample 1

This code sample illustrates the basic usage of the binary vector equality operator"""

# print(tl.binary_vector_equal([1, 0, 1, 0, 0], [1, 0, 1, 0, 0]))

v1 = BV([1, True, 0])
print(v1)
v2 = BV(size=7)
print(v2)
v3 = BV(size=5, default_value=1)
print(v3)
