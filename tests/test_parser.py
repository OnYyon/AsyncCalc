import unittest
from src.infix_to_postfix import Parser
from src.errors import ParserError


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_simple(self):
        tokens = [
            ("NUMBER", "42", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["42"])

    def test_add(self):
        tokens = [
            ("NUMBER", "2", 0, 0),
            ("OPERATOR", "+", 0, 0),
            ("NUMBER", "3", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["2", "3", "+"])

    def test_sub(self):
        tokens = [
            ("NUMBER", "5", 0, 0),
            ("OPERATOR", "-", 0, 0),
            ("NUMBER", "1", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["5", "1", "-"])

    def test_mul(self):
        tokens = [
            ("NUMBER", "2", 0, 0),
            ("OPERATOR", "+", 0, 0),
            ("NUMBER", "3", 0, 0),
            ("OPERATOR", "*", 0, 0),
            ("NUMBER", "4", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["2", "3", "4", "*", "+"])

    def test_parentheses(self):
        tokens = [
            ("LEFT_PARENTHESIS", "(", 0, 0),
            ("NUMBER", "2", 0, 0),
            ("OPERATOR", "+", 0, 0),
            ("NUMBER", "3", 0, 0),
            ("RIGHT_PARENTHESIS", ")", 0, 0),
            ("OPERATOR", "*", 0, 0),
            ("NUMBER", "4", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["2", "3", "+", "4", "*"])

    def test_unary_minus(self):
        tokens = [
            ("OPERATOR", "-", 0, 0),
            ("NUMBER", "5", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["5", "~"])


    def test_nested_unary_and_parentheses(self):
        tokens = [
            ("OPERATOR", "-", 0, 0),
            ("LEFT_PARENTHESIS", "(", 0, 0),
            ("OPERATOR", "-", 0, 0),
            ("NUMBER", "3", 0, 0),
            ("RIGHT_PARENTHESIS", ")", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["3", "~", "~"])

    def test_nested_pow(self):
        tokens = [
            ("LEFT_PARENTHESIS", "(", 0, 0),
            ("NUMBER", "3", 0, 0),
            ("OPERATOR", "**", 0, 0),
            ("NUMBER", "4", 0, 0),
            ("RIGHT_PARENTHESIS", ")", 0, 0),
            ("OPERATOR", "**", 0 ,0),
            ("NUMBER", "5", 0, 0),
            ("EOF", "", 0, 0)
        ]
        self.assertEqual(self.parser.calculate(tokens), ["3", "4", "**", "5", "**"])

    def test_unexpected_token(self):
        tokens = [
            ("NUMBER", "2", 0, 0),
            ("OPERATOR", "+", 0, 0),
            ("OPERATOR", "+", 0, 0),
            ("EOF", "", 0, 0)
        ]
        with self.assertRaises(ParserError):
            self.parser.calculate(tokens)

    def test_missing_right_parenthesis(self):
        tokens = [
            ("LEFT_PARENTHESIS", "(", 0, 0),
            ("NUMBER", "2", 0, 0),
            ("EOF", "", 0, 0)
        ]
        with self.assertRaises(ParserError):
            self.parser.calculate(tokens)

    def test_missing_left_parenthesis(self):
        tokens = [
            ("LEFT_PARENTHESIS", "(", 0, 0),
            ("NUMBER", "2", 0, 0),
            ("RIGHT_PARENTHESIS", ")", 0, 0),
            ("RIGHT_PARENTHESIS", ")", 0, 0),
            ("EOF", "", 0, 0)
        ]
        with self.assertRaises(ParserError):
            self.parser.calculate(tokens)

    def test_empty_expression(self):
        tokens = [("EOF", "", 1, 1)]
        with self.assertRaises(ParserError):
            self.parser.calculate(tokens)


if __name__ == '__main__':
    unittest.main()
