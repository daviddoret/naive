from unittest import TestCase
import labeling_function
from _trashcan import atom


class Test(TestCase):
    def test_labeling_function_1(self):
        AP = atom.AtomSet(['Red', 'Green', 'Blue'])
        S = space.LabelSpace(6)
        L = labeling_function.LabelingFunction(AP, S)
        L.link_label_to_state('Red', 's4')
        print(L.BinaryMatrix)
        print(L.CheckLabel('Red', 's4'))
        print(L.CheckLabel('Blue', 's4'))
        print(L.CheckLabel('Red', 's2'))