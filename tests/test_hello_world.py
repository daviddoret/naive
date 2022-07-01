from unittest import TestCase
import src.naive.hello_world as hi


class Test(TestCase):
    def test_say_hello(self):
        self.assertEqual(hi.say_hello(), "hello anonymous")
        self.assertEqual(hi.say_hello('foobar'), "hello foobar")
