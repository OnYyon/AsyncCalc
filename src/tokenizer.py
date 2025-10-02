import re
from typing import Iterator
from src.errors import EmptyExpression
from src.constants import EXPRESSION_TOKEN

def tokenize(expression: str) -> Iterator[re.Match[str]]:
    """
    Разбить строку на токены: числа или операторы.
    :param expression: Строка выражения.
    :return: Итератор, который дает строку числа или оператора.
    """
    if not expression or not expression.strip():
        raise EmptyExpression

    pattern = re.compile(EXPRESSION_TOKEN, re.VERBOSE)
    # tokens = [m.group(1) for m in pattern.finditer(expression)]
    # print(pattern, tokens)
    return pattern.finditer(expression)
