import json
from typing import Iterator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse

from src.api.server import mgr
from src.api.utils.models import Expression, ExpressionsResponse, ExpressionRequset, ListExpression


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    mgr.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/add/", response_model=ExpressionsResponse)
def add_new_expression(data: ExpressionRequset) -> ExpressionsResponse:
    expression = data.expression.strip()

    task_id = mgr.add_task(expression)

    return ExpressionsResponse(
        task_id = task_id
    )

@app.get("/api/v1/getByID/{task_id}", response_model=Expression)
def get_by_id(task_id: str) -> Expression:
    task_id, expr, value, error, text_error = mgr.get_task_by_id(task_id)

    return Expression(
        task_id = task_id,
        expression = expr,
        result = value,
        have_error=False,
        text_error=text_error
    )


@app.get("/api/v1/getList")
def get_all_expressions() -> StreamingResponse:
    def generate_ndjson() -> Iterator[str]:
        for task in mgr.get_all_tasks():
            yield json.dumps(task) + "\n"
    return StreamingResponse(generate_ndjson())
