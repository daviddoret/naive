from unittest import TestCase
import naive.hello_world as hi


class Test(TestCase):
    def test_say_hello(self):
        self.assertEqual(hi.say_hello(), "hello world")
