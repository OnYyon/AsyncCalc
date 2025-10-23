import unittest

from src.tokenizer import tokenize
from src.calculate import evaluate_rpn
from src.infix_to_postfix import  Parser



class TestComplex(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def _calc(self, expr: str) -> float:
        return evaluate_rpn(self.parser.calculate(tokenize(expr)))

    def test_simple(self):
        self.assertEqual(self._calc("1+2"), 3)

    def test_middle(self):
        self.assertEqual(self._calc("-1*(2-3)**5"), 1)

    def test_hard(self):
        self.assertEqual(self._calc("((7+1)/(2+2)*4)/8*(32-((4+12)*2))-1+((7+1)/(2+2)*4)/8*(32-((4+12)*2))-1"), -2)
