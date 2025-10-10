from src.tokenizer import tokenize
from src.errors import ParserError


class Parser:
    """
    Текущая EBNF грамматика:
    <expression> ::= <term> {("+" | "-" ) <term>}
    <term> ::= <factor> {("*" | "/") <factor>}
    <factor> ::= <primary> {"^" factor}
    <primary> ::= NUMBER
    """
    def __init__(self, tokens: list[tuple[str, str, int, int]]):
        self.rpn: list[str] = []
        self.index: int = 0
        self.tokens: list[tuple[str, str, int, int]] = tokens
        self.token: tuple[str, str, int, int] = self.tokens[0]

        self.parse_expression()

    def consume(self, check_type: str) -> str | None:
        """
        Функция для получения текущего токена с проверкой на ожидаймый тип
        :param check_type: какой тип ожидаем
        :return: строку или None в случаи выхода за границу
        """
        if self.token[0] != check_type:
            raise ParserError(f"unexpected token: {self.token[1]} expected {check_type} {self.token[2]}:{self.token[3]}")

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

        while self.token[0] == "OPERATOR" and self.token[1] in ("+", "-"):
            op = self.consume("OPERATOR")
            self.parse_term()
            self.rpn.append(op)

    def parse_term(self):
        """
        <term> ::= <factor> {("*" | "/") <factor>}
        Обрабатываем умножение/деление.
        """
        self.parse_factor()

        while self.token[0] == "OPERATOR" and self.token[1] in ("/", "*"):
            op = self.consume("OPERATOR")
            self.parse_factor()
            self.rpn.append(op)

    def parse_factor(self):
        """
        <factor> ::= <primary> {"**" <factor>}
        Обрабатываем возведение в степень
        """
        self.parse_primary()

        while self.token[0] == "OPERATOR" and self.token[1] == "**":
            op = self.consume("OPERATOR")
            self.parse_factor()
            self.rpn.append(op)

    def parse_primary(self):
        """
        Добавляем число в стек RPN
        """
        self.rpn.append(self.consume("NUMBER"))

    def get_rpn(self) -> list[str]:
        return  self.rpn


# TODO: Delete after testing
if __name__ == "__main__":
    import operator
    parser = Parser(tokenize("100 * 100 + 100 ** 2 ** 2"))
    rpn = parser.get_rpn()
    print(rpn)
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
