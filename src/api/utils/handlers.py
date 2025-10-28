from src.api.server import app
from src.api.server import mgr
from src.api.utils.models import Expression, ExpressionsResponse, ExpressionRequset


@app.post("/api/v1/add/", response_model=ExpressionsResponse)
def add_new_expression(data: ExpressionRequset) -> ExpressionsResponse:
    expression = data.expression.strip()

    task_id = mgr.add_task(expression)

    return ExpressionsResponse(
        task_id = task_id
    )

@app.post("/api/v1/getByID/{task_id}", response_model=Expression)
def get_by_id(task_id: str) -> Expression:
    task_id, expr, value, error, text_error = mgr.get_task_by_id(task_id)

    return Expression(
        task_id = task_id,
        expression = expr,
        result = value,
        have_error=False,
        text_error=text_error
    )
