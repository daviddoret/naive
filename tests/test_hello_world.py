from unittest import TestCase
import src.naive.hello_world as hi


class Test(TestCase):
    def test_say_hello(self):
        self.assertEqual(hi.hello_world(), "hello anonymous")
        self.assertEqual(hi.hello_world('foobar'), "hello foobar")
