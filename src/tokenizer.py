import re
from src.constants import EXPRESSION_TEMPLATE
from src.errors import ExpressionError, EmptyExpressionError


def tokenize(expression: str) -> list[tuple[str, str, int, int]]:
    """
    Разбить строку на токены: числа или операторы.
    Общая структура токенов: (type, token, start_pos, end_pos)
    Если токен число, то кладем: ("NUMBER", ...)
    Если токен оператор, то кладем: ("OPERATOR", ...)
    Если токен скобка, то кладем: ("LEFT_PARENTHESIS"/"RIGHT_PARENTHESIS", ...)
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
            if not expression[pos:pos + 10].strip():
                raise ExpressionError("end")
            raise ExpressionError(expression[pos:pos+5])

        t = m.group(1)
        pos = m.end()

        if t[0].isdigit():
            out.append(("NUMBER", t, m.start(), m.end()))
        elif t == ")":
            out.append(("RIGHT_PARENTHESIS", t, m.start(), m.end()))
        elif t == "(":
            out.append(("LEFT_PARENTHESIS", t, m.start(), m.end()))
        else:
            out.append(("OPERATOR", t, m.start(), m.end()))

    out.append(("EOF", "", -1, -1))
    return out
