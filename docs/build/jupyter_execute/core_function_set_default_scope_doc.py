#!/usr/bin/env python
# coding: utf-8

# In[1]:


initial_scope = naive.core.get_default_scope()
print(f'The initial scope was: {initial_scope}')

naive.core.set_default_scope('my_scope')
print('Do something...')

naive.core.set_default_scope('another_scope')
print('Do something...')

naive.core.set_default_scope(initial_scope)
print('Do something...')

