Usage
=====

.. _installation:

Installation
------------

To use Naive, first install it using pip:

.. code-block:: console

   (.venv) $ pip install naive

Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``kripke_structure.coerce_binary_value()`` function:

.. autofunction:: ks.coerce_binary_value

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import kripke_structure
>>> print(kripke_structure.coerce_binary_value([1, 0, 1]))
[True, False, True]

