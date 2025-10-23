from src.tokenizer import tokenize
from src.calculate import evaluate_rpn
from src.infix_to_prefix import Parser
from src.errors import ExpressionError, ParserError


def main():
    parser = Parser()
    while (exp := input("Введите свое выражение:")) and exp not in ["end", "q"]:
        try:
            answer = evaluate_rpn(parser.calculate(tokenize(exp)))
        except (ExpressionError, ParserError) as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            break
        print(f"Ответ: {answer}")


if __name__ == "__main__":
    main()
