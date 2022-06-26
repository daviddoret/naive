Type Library
===================================

TODO: Include documentation

.. note::

   This project is under active development.

.. currentmodule:: type_library

Types, Type Aliases, TypeVars, and NewTypes
-------------------------------------------

Often, we need a particular class or type to make it semantically clear in our code that we are manipulating conceptual objects of a particular nature. But as often, native types and classes satisfy our technical needs. `NewTypes <https://docs.python.org/3/library/typing.html#typing.NewType>`_ constitute an efficient solution to this issue. (References: `Stackoverflow question <https://stackoverflow.com/questions/58755948/what-is-the-difference-between-typevar-and-newtype>`_).

.. autosummary::
    :toctree: pages
    :recursive:

    AtomicProperty
    AtomicPropertyInput
    AtomicPropertySet
    AtomicPropertySetInput
    BinaryMatrix
    BinaryMatrixInput
    BinarySquareMatrix
    BinarySquareMatrixInput
    BinaryValue
    BinaryValueInput
    BinaryVector
    BinaryVectorInput
    Element
    ElementInput
    IncidenceVector
    IncidenceVectorInput
    IndexPosition
    IndexPositionInput
    Set
    SetInput
    SetOrIV
    SetOrIVInput
    State
    StateInput
    StateSet
    StateSetInput


Functions
---------

.. autosummary::
    :toctree: pages
    :recursive:

    coerce_atomic_property
    coerce_atomic_property_set
    coerce_binary_matrix
    coerce_binary_square_matrix
    coerce_binary_value
    coerce_binary_vector
    coerce_element
    coerce_incidence_vector
    coerce_set
    coerce_state
    coerce_state_set
    flatten