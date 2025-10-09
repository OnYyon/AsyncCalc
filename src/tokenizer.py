import re
from src.constants import EXPRESSION_TEMPLATE
from src.errors import ExpressionError, EmptyExpressionError


def tokenize(expression: str) -> list[tuple[str, str, int, int]]:
    """
    Разбить строку на токены: числа или операторы.
    :param expression: Строка выражения.
    :return: список токенов
    """
    if not expression or not expression.strip():
        raise EmptyExpressionError

    pattern = re.compile(EXPRESSION_TEMPLATE, re.VERBOSE)
    pos: int = 0
    out: list[tuple[str, str, int, int]] = []

    while pos < len(expression):
        m = pattern.match(expression, pos)
        if not m:
            raise ExpressionError(expression[pos:pos+10])

        t = m.group(1)
        pos = m.end()

        if t[0].isdigit():
            out.append(("NUMBER", t, m.start(), m.end()))
        else:
            out.append(("OPERATOR", t, m.start(), m.end()))

    out.append(("EOF", "", -1, -1))
    return out
