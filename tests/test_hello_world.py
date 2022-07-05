from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_say_hello(self):
        self.assertEqual(naive.hello_world(), "hello anonymous")
        self.assertEqual(naive.hello_world('foobar'), "hello foobar")
