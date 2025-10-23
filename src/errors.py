class ExpressionError(Exception):
    """
    Ошибки связанные с неправильностью вводимого выражения
    """

    def __init__(self, src: str):
        self.part_of_string = src

    def __str__(self) -> str:
        print(self.part_of_string)
        return f"You have error near: {self.part_of_string}"


class EmptyExpressionError(Exception):
    def __str__(self) -> str:
        return "Empty string"


class ParserError(Exception):
    ...
