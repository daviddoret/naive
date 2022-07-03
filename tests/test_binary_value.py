from unittest import TestCase
import src.naive as naive


class TestBinaryValue(TestCase):
    def test_init(self):
        b = naive.BinaryVariable(True)
