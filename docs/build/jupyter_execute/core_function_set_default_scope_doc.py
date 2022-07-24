#!/usr/bin/env python
# coding: utf-8

# In[1]:


import naive
name = 'world'
print('hello ' + name + '!')
naive.core.set_default_scope('my_scope')
naive.core.set_default_scope('another_scope')

