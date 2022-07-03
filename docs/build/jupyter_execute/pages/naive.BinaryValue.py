#!/usr/bin/env python
# coding: utf-8

# In[1]:


import naive
b1 = naive.BV(False)
b2 = naive.BV(True)
print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')
b2.bool = True
print(f'(b1 = b2) = ({b1} = {b2}) = {b1 == b2}')

