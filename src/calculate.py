from src.errors import ParserError


def operators(operation: str, op1: float, op2: float | None) -> float:
    """
    Для получения результата операций.
    При op2 is None счиатаем опрецию унарную.
    :param operation: операция
    :param op1: опреранд 1
    :param op2: опреранд 2
    :return: возвращаем результат опреции
    """
    if op2 is None:
        return -1 * op1
    match operation:
        case "+":
            return op2 + op1
        case "-":
            return op2 - op1
        case "*":
            return op2 * op1
        case "/":
            if op1 == 0:
                raise ParserError("Are you sure? Division by zero")
            return op2 / op1
        case "%":
            if op1 == 0:
                raise ParserError("Are you sure? Division by zero")
            return op2 % op1
        case "//":
            return op2 // op1
        case "**":
            return op2 ** op1
        case _:
            raise ParserError(f"Unknown operator: {operation}")


def evaluate_rpn(rpn: list[str]) -> float:
    """
    Получения ответа из обратной полльской нотации
    :param rpn: список с выраженим в RPN
    """
    stack: list[float] = []
    for token in rpn:
        if token[0].isdigit():
            stack.append(float(token))
        elif token == "~":
            stack.append(operators(token, stack.pop(), None))
        else:
            stack.append(operators(token ,stack.pop(), stack.pop()))
    if len(stack) > 1:
        raise ParserError(f"Unprocessable operator: {stack}")
    return stack[0]
