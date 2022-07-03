from __future__ import absolute_import
from unittest import TestCase
import src.naive as naive

class TestNaturalVector1(TestCase):
    def test_1(self):
        self.assertEqual(str(naive.NV1([1, 3, 2, 2])), '{1, 3, 2, 2}')
