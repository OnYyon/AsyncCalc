class ExpressionError(Exception):
    """
    Ошибки связанные с неправильностью вводимого выражения
    """
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"You have error near: start - {self.start}, end - {self.end}"


class EmptyExpression(Exception):
    def __str__(self) -> str:
        return "Your expression is empty"
