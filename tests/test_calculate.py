import unittest

from src.calculator.errors import ParserError
from src.calculator.calculate import evaluate_rpn


class TestParser(unittest.TestCase):
    def setUp(self):
        self.calc = evaluate_rpn

    def test_simple(self):
        self.assertEqual(self.calc(['1', '2', '+']), 3)

    def test_unary_minus(self):
        self.assertEqual(self.calc(['2', '3', '+', '~', '1', '+']), -4)

    def test_zero_division(self):
        with self.assertRaises(ParserError):
            self.calc(['2', '0', '/', '~', '1', '+'])

    def test_zero_module(self):
        with self.assertRaises(ParserError):
            self.calc(['2', '0', '%', '~', '1', '+'])
