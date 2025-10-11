from typing import Callable
from src.tokenizer import tokenize
from src.errors import ParserError


class Parser:
    """
    Текущая EBNF грамматика:
    <expression> ::= <term> {("+" | "-" ) <term>}
    <term> ::= <factor> {("*" | "/") <factor>}
    <factor> ::= <primary> {"^" factor}
    <primary> ::= NUMBER / <parenthesizedExpression>
    <parenthesizedExpression> ::= "(" <expression> ")"
    """

    def __init__(self, tokens: list[tuple[str, str, int, int]]):
        self.rpn: list[str] = []
        self.index: int = 0
        self.tokens: list[tuple[str, str, int, int]] = tokens
        self.token: tuple[str, str, int, int] = self.tokens[0]

        self._tracer: list[Callable] = [self.parse_expression]

        self.parse_expression()

    def consume(self, check_type: str) -> str | None:
        """
        Функция для получения текущего токена с проверкой на ожидаймый тип
        :param check_type: какой тип ожидаем
        :return: строку или None в случаи выхода за границу
        """
        if self.token[0] != check_type:
            raise ParserError(
                f"unexpected token: {self.token[1]} expected {check_type} {self.token[2]}:{self.token[3]}")

        t = self.token[:]
        self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
            return t[1]
        return None

    def parse_expression(self):
        """
        <expression> ::= <term> {("+" | "-") <term>}
        Обрабатываем сложение/вычитание.
        """
        self.parse_term()
        self._tracer.append(self.parse_term)

        while self.token[0] == "OPERATOR" and self.token[1] in ("+", "-"):
            op = self.consume("OPERATOR")
            self.parse_term()
            self._tracer.append(self.parse_term)
            self.rpn.append(op)

    def parse_term(self):
        """
        <term> ::= <factor> {("*" | "/") <factor>}
        Обрабатываем умножение/деление.
        """
        self.parse_factor()
        self._tracer.append(self.parse_factor)

        while self.token[0] == "OPERATOR" and self.token[1] in ("/", "*"):
            op = self.consume("OPERATOR")
            self.parse_factor()
            self._tracer.append(self.parse_factor)
            self.rpn.append(op)

    def parse_factor(self):
        """
        <factor> ::= <primary> {"**" <factor>}
        Обрабатываем возведение в степень
        """
        self.parse_primary()
        self._tracer.append(self.parse_primary)

        while self.token[0] == "OPERATOR" and self.token[1] == "**":
            op = self.consume("OPERATOR")
            self.parse_factor()
            self._tracer.append(self.parse_factor)
            self.rpn.append(op)

    def parse_primary(self):
        """
        Добавляем число в стек RPN
        """

        if self.token[0] == "LEFT_PARENTHESIS":
            self.parse_parenthesized_expression()
            self._tracer.append(self.parse_parenthesized_expression)
            return

        self.rpn.append(self.consume("NUMBER"))

    def parse_parenthesized_expression(self):
        self.consume("LEFT_PARENTHESIS")
        self.parse_expression()
        self._tracer.append(self.parse_expression)
        self.consume("RIGHT_PARENTHESIS")

    def get_rpn(self) -> list[str]:
        return self.rpn

    def _get_tracer(self) -> list[Callable]:
        return self._tracer


# TODO: Delete after testing
if __name__ == "__main__":
    import operator
    from pprint import pprint

    parser = Parser(tokenize("((1 + 2) + (3))"))
    rpn = parser.get_rpn()
    pprint(parser._get_tracer())
    stack = []
    d = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "**": operator.pow,
    }
    for token in rpn:
        if token[0].isdigit():
            stack.append(float(token))
        else:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(d[token](op1, op2))
    print(stack)
