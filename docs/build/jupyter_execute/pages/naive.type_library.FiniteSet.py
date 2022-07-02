#!/usr/bin/env python
# coding: utf-8

# In[1]:


import naive.type_library as tl


# In[2]:


# If nothing is passed to the constructor, an empty set is returned:
s = tl.FiniteSet()
print(s)


# In[3]:


# Finite sets may be built from a series of string-equivalent objects:
s = tl.FiniteSet(u'Platypus', 'Euler', 'Boson')
print(s)


# In[4]:


# ...or iterable objects:
s = tl.FiniteSet(['Platypus', 'Euler', 'Boson'])
print(s)


# In[5]:


# FS is shorthand for FiniteSet:
s = tl.FS(u'FS', 'FiniteSet')
print(s)


# In[6]:


# Mathematical sets are unordered by definition,
# but naive implementation is automatically ordered:
s = tl.FiniteSet('h', 'g', 'b', 'a', 'c', 'f', 'g')
print(s)
# The reason for this design choice are:
#  1) readability,
#  2) compatibility with incidence vectors.


# In[7]:


# The constructor is adaptive and flattens whatever input it gets:
s = tl.FS('a', 'b', 'c', ['d', 'e', ['f']])
print(s)


# In[8]:


# The size shortcut helps create sets of canonically named elements:
s = tl.FS(size=5)
print(s)


# In[9]:


# ...with a custom prefix:
s = tl.FS(size=3, prefix='x')
print(s)


# In[10]:


# ...0-based index:
s = tl.FS(size=3, prefix='y', init=0)
print(s)


# In[11]:


# Note that spaces (" ") and commas (",") are forbidden in element names to avoid ambiguity:
s = tl.FS('hack, the, list')
print(s)


# In[12]:


# Note that indexes are voluntarily padded for easier alphanumeric ordering:
s = tl.FS(size=12, prefix='y', init=1)
print(s)

