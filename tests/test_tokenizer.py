import unittest

from src.errors import ExpressionError, EmptyExpressionError
from src.tokenizer import tokenize


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.func = tokenize

    def test_simple(self):
        self.assertEqual(self.func("1+2"), [("NUMBER", "1", 0, 1),
                                                    ("OPERATOR", "+", 1, 2),
                                                    ("NUMBER", "2", 2, 3),
                                                    ("EOF", "", -1, -1)])

    def test_with_parenthesis(self):
        self.assertEqual(self.func("(1+2)"), [("LEFT_PARENTHESIS", "(", 0, 1),
                                                    ("NUMBER", "1", 1, 2),
                                                    ("OPERATOR", "+", 2, 3),
                                                    ("NUMBER", "2", 3, 4),
                                                    ("RIGHT_PARENTHESIS", ")", 4, 5),
                                                    ("EOF", "", -1, -1)])

    def test_with_unary_operation(self):
        self.assertEqual(self.func("-1+2"), [("OPERATOR", "-", 0, 1),
                                                    ("NUMBER", "1", 1, 2),
                                                    ("OPERATOR", "+", 2, 3),
                                                    ("NUMBER", "2", 3, 4),
                                                    ("EOF", "", -1, -1)])

    def test_check_all_correct_symbols(self):
        self.assertEqual(self.func("-(1+2)%8//2-4**4*4/4"), [('OPERATOR', '-', 0, 1),
                                                             ('LEFT_PARENTHESIS', '(', 1, 2),
                                                             ('NUMBER', '1', 2, 3),
                                                             ('OPERATOR', '+', 3, 4),
                                                             ('NUMBER', '2', 4, 5),
                                                             ('RIGHT_PARENTHESIS', ')', 5, 6),
                                                             ('OPERATOR', '%', 6, 7),
                                                             ('NUMBER', '8', 7, 8),
                                                             ('OPERATOR', '//', 8, 10),
                                                             ('NUMBER', '2', 10, 11),
                                                             ('OPERATOR', '-', 11, 12),
                                                             ('NUMBER', '4', 12, 13),
                                                             ('OPERATOR', '**', 13, 15),
                                                             ('NUMBER', '4', 15, 16),
                                                             ('OPERATOR', '*', 16, 17),
                                                             ('NUMBER', '4', 17, 18),
                                                             ('OPERATOR', '/', 18, 19),
                                                             ('NUMBER', '4', 19, 20),
                                                             ('EOF', '', -1, -1)])

    def test_incorrect_symbol(self):
        with self.assertRaises(ExpressionError):
            self.func("2^8")
            self.func("asdf")

    def test_empty_expression(self):
        with self.assertRaises(EmptyExpressionError):
            self.func("")
            self.func("   ")


if __name__ == "__main__":
    unittest.main()
