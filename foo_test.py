import unittest
from hypothesis import given,  strategies

from foo import Foo


class TestFoo(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(Foo().hello(), "hello")

    @given(strategies.integers(), strategies.integers())
    def test_add_commutative(self, a, b):
        self.assertEqual(Foo().add(a, b), Foo().add(b, a))
