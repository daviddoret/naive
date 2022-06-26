from unittest import TestCase
import hello_world


class Test(TestCase):
    def test_say_hello(self):
        self.assertEqual(hello_world.say_hello(), "hello world")
