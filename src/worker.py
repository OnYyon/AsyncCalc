import multiprocessing

from src.calculator.tokenizer import tokenize
from src.calculator.calculate import evaluate_rpn
from src.calculator.infix_to_postfix import Parser
from src.calculator.errors import ParserError, ExpressionError, EmptyExpressionError


def worker(name: str, task_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue):
    parser = Parser()
    while True:
        task = task_queue.get()
        if task is None:
            break
        task_id, expr = task
        try:
            result = evaluate_rpn(parser.calculate(tokenize(expr)))
            result_queue.put((task_id, expr, result, False, ""))
        except (ParserError, ExpressionError, EmptyExpressionError) as e:
            result_queue.put((task_id, expr, -1, True, e))
        except Exception as e:
            raise e
