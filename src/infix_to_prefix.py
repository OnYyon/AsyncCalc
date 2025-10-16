from typing import Callable

from src.tokenizer import tokenize
from src.errors import ParserError


class Parser:
    """
    Для разбора токенов рекурсивным спуском
    Текущая EBNF грамматика:
    <expression> ::= <term> {("+" | "-" ) <term>}
    <term> ::= <factor> {("*" | "/") <factor>}
    <factor> ::= <unary> {"^" factor}
    <primary> ::= NUMBER / <parenthesized> / <unary>
    <parenthesized> ::= "(" <expression> ")"
    <unary> ::= ("-" | "+")  <primary>
    """

    def __init__(self, tokens: list[tuple[str, str, int, int]]):
        self.rpn: list[str] = []
        self.index: int = 0
        self.tokens: list[tuple[str, str, int, int]] = tokens
        self.token: tuple[str, str, int, int] = self.tokens[0]

        self._tracer: list[Callable[[], None]] = [self.parse_expression]

        self.parse_expression()

    def consume(self, check_type: str) -> str:
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
        self.token = self.tokens[self.index]
        return t[1]

    def parse_expression(self) -> None:
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

    def parse_term(self) -> None:
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

    def parse_factor(self) -> None:
        """
        <factor> ::= <unary> {"**" <factor>}
        Обрабатываем возведение в степень
        """
        self.parse_primary()
        self._tracer.append(self.parse_primary)

        while self.token[0] == "OPERATOR" and self.token[1] == "**":
            op = self.consume("OPERATOR")
            self.parse_factor()
            self._tracer.append(self.parse_factor)
            self.rpn.append(op)

    def parse_primary(self) -> None:
        """
        Добавляем число в стек RPN
        """
        if self.token[0] == "LEFT_PARENTHESIS":
            self.parse_parenthesized_expression()
            self._tracer.append(self.parse_parenthesized_expression)
            return
        if self.token[0] == "OPERATOR" and self.token[1] == "-" or self.token[1] == "+":
            self.parse_unary_expression()
            self._tracer.append(self.parse_unary_expression)
            return

        self.rpn.append(self.consume("NUMBER"))

    def parse_parenthesized_expression(self) -> None:
        """
        <parenthesizedExpression> ::= "(" <expression> ")"
        Обрабатываем скобки.
        """
        self.consume("LEFT_PARENTHESIS")
        self.parse_expression()
        self._tracer.append(self.parse_expression)
        self.consume("RIGHT_PARENTHESIS")

    def parse_unary_expression(self) -> None:
        """
        <unary> ::= ("-"|"+") <primary>
        Обрабатываем унарные +/-.
        Обратите внимание у унарных операций высший приоритет
        Тут такое `допущение` так как унарный + не влияет на ответ, то мы не будем его добавлять
        """
        op = self.consume("OPERATOR")
        self.parse_primary()
        if op == "-":
            self.rpn.append("~")

    def get_rpn(self) -> list[str]:
        return self.rpn

    def _get_tracer(self) -> list[Callable[[], None]]:
        return self._tracer


# TODO: Delete after testing
if __name__ == "__main__":
    import operator
    from pprint import pprint

    tokens = tokenize("2**3**2")
    parser = Parser(tokens)
    rpn = parser.get_rpn()
    pprint(parser._get_tracer())
    print(tokens, rpn)
    stack: list[float]= []
    d: dict[str, Callable[..., float]] = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "**": operator.pow,
        "~": operator.neg,
    }
    for token in rpn:
        if token[0].isdigit():
            stack.append(float(token))
        elif token == "~":
            op = stack.pop()
            stack.append(d[token](op))
        else:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(d[token](op1, op2))
    print(stack)
