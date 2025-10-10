from src.tokenizer import tokenize
from src.errors import ParserError


class Parser:
    """
    Текущая EBNF грамматика:
    <expression> ::= <term> {("+" | "-" ) <term>}
    <term> ::= <primary> {("*" | "/") <primary>}
    <primary> ::= NUMBER
    """
    def __init__(self, tokens: list[tuple[str, str, int, int]]):
        self.rpn: list[str] = []
        self.index: int = 0
        self.tokens: list[tuple[str, str, int, int]] = tokens
        self.token: tuple[str, str, int, int] = self.tokens[0]

        self.parse_expression()

    def consume(self, check_type: str):
        if self.token[0] != check_type:
            raise ParserError(f"unexpected token: {self.token[1]} expected {check_type} {self.token[2]}:{self.token[3]}")

        t = self.token[:]
        self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
            return t[1]
        return None

    def parse_expression(self):
        self.parse_term()

        while self.token[0] == "OPERATOR":
            op = self.consume("OPERATOR")
            self.parse_term()
            self.rpn.append(op)

    def parse_term(self):
        self.parse_primary()
        while self.token[0] == "OPERATOR" and (self.token[1] == "/" or self.token[1] == "*"):
            op = self.consume("OPERATOR")
            self.parse_primary()
            self.rpn.append(op)

    def parse_primary(self):
        self.rpn.append(self.consume("NUMBER"))

    def get_rpn(self) -> list[str]:
        return  self.rpn


# TODO: Delete after testing
if __name__ == "__main__":
    parser = Parser(tokenize("123424 * 124.1234 + 341 + 4324 * 432"))
    print(parser.get_rpn())
