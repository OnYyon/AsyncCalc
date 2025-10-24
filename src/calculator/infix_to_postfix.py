from src.calculator.errors import ParserError


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
    rpn: list[str]
    index: int
    tokens: list[tuple[str, str, int, int]]
    token: tuple[str, str, int, int]

    def __init__(self):
        self._clean()

    def calculate(self, tokens: list[tuple[str, str, int, int]]) -> list[str]:
        self._clean()
        self.tokens = tokens
        self.token = tokens[0]
        self.parse_expression()
        if self.token[0] != "EOF":
            raise ParserError(f"Unexpected token: {self.token[1]} expected EOF")
        return self.rpn

    def consume(self, check_type: str) -> str:
        """
        Функция для получения текущего токена с проверкой на ожидаймый тип
        :param check_type: какой тип ожидаем
        :return: строку или None в случаи выхода за границу
        """
        if self.token[0] != check_type:
            raise ParserError(
                f"Unexpected token: {self.token[1]} expected {check_type} {self.token[2]}:{self.token[3]}")

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

        while self.token[0] == "OPERATOR" and self.token[1] in ("+", "-"):
            op = self.consume("OPERATOR")
            self.parse_term()
            self.rpn.append(op)

    def parse_term(self) -> None:
        """
        <term> ::= <factor> {("*" | "/") <factor>}
        Обрабатываем умножение/деление.
        """
        self.parse_factor()

        while self.token[0] == "OPERATOR" and self.token[1] in ("/", "*", "//", "%"):
            op = self.consume("OPERATOR")
            self.parse_factor()
            self.rpn.append(op)

    def parse_factor(self) -> None:
        """
        <factor> ::= <unary> {"**" <factor>}
        Обрабатываем возведение в степень
        """
        self.parse_primary()

        while self.token[0] == "OPERATOR" and self.token[1] == "**":
            op = self.consume("OPERATOR")
            self.parse_factor()
            self.rpn.append(op)

    def parse_primary(self) -> None:
        """
        Добавляем число в стек RPN
        """
        if self.token[0] == "LEFT_PARENTHESIS":
            self.parse_parenthesized_expression()
            return
        if self.token[0] == "OPERATOR" and self.token[1] == "-" or self.token[1] == "+":
            self.parse_unary_expression()
            return

        self.rpn.append(self.consume("NUMBER"))

    def parse_parenthesized_expression(self) -> None:
        """
        <parenthesizedExpression> ::= "(" <expression> ")"
        Обрабатываем скобки.
        """
        self.consume("LEFT_PARENTHESIS")
        self.parse_expression()
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

    def _clean(self):
        """
        Сбрасывет занчения для получения новго
        """
        self.rpn = []
        self.index = 0
        self.tokens = []
