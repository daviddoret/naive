import naive.type_library as tl
print(u'If nothing is passed to the constructor, an empty set is returned:')
s = tl.FiniteSet()
print(s)

print(u'\nFinite sets may be built from a series of string-equivalent objects:')
s = tl.FiniteSet(u'Platypus', 'Euler', 'Boson')
print(s)

print(u'\n...or iterable objects:')
s = tl.FiniteSet(['Platypus', 'Euler', 'Boson'])
print(s)

print(u'\nFS is shorthand for FiniteSet:')
s = tl.FS(u'FS', 'FiniteSet')
print(s)

print(u'\nMathematical sets are unordered by definition, but this implementation is automatically ordered:')
s = tl.FiniteSet('h', 'g', 'b', 'a', 'c', 'f', 'g')
print(s)
print('The reason for this design choice are:')
print(' 1) readability,')
print(' 2) compatibility with incidence vectors.')

print('\nThe constructor is adaptive and flattens whatever input it gets:')
s = tl.FS('a', 'b', 'c', ['d', 'e', ['f']])
print(s)

print('\nThe size shortcut helps create sets of canonically named elements:')
s = tl.FS(size=5)
print(s)

print('\n...with a custom prefix:')
s = tl.FS(size=3, prefix='v')
print(s)

print('\n...0-based indexes:')
s = tl.FS(size=3, prefix='y', init=0)
print(s)

print('\nNote that spaces (" ") and commas (",") are forbidden in element names to avoid ambiguity:')
s = tl.FS('hack, the, list')
print(s)

print('\nNote that indexes are voluntarily padded for easier alphanumeric ordering:')
s = tl.FS(size=12, prefix='y', init=1)
print(s)
