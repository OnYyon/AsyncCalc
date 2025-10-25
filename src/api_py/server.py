from fastapi import FastAPI

from src.api_py.utils.models import Expression, ExpressionsResponse, ExpressionRequset, ListExpression
from src.api_py.utils.manager import mgr


app = FastAPI()

@app.post("/api/v1/add/", response_model=ExpressionsResponse)
def add_new_expression(data: ExpressionRequset) -> ExpressionsResponse:
    expression = data.expression.strip()

    task_id = mgr.add_task(expression)

    return ExpressionsResponse(
        TaskID = task_id
    )

@app.post("/api/v1/getByID/{task_id}", response_model=Expression)
def get_by_id(task_id: str) -> Expression:
    task_id, expr, value, error = mgr.get_task_by_id(task_id)

    if error:
        return Expression(
            task_id = task_id,
            expression = expr,
            result = -1,
            have_error = True,
        )
    return Expression(
        task_id = task_id,
        expression = expr,
        result = value,
        have_error=False,
    )

@app.get("/api/v1/getList/")
def get_list() -> ListExpression:
    d = mgr.get_all_tasks()
    return ListExpression(
        d = d,
    )
