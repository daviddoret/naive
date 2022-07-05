#!/usr/bin/env python
# coding: utf-8

# In[1]:


import naive
b1 = naive.BC(False)
b2 = naive.BC(True)
print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')
b2.bool = True
print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')

