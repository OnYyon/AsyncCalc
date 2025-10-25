from pydantic import BaseModel

class ExpressionRequset(BaseModel):
    expression: str | None = None

class ExpressionsResponse(BaseModel):
    TaskID: str | None = None

class Expression(BaseModel):
    task_id: str | None = None
    expression: str | None = None
    result: float | None = None
    have_error: bool | None = None

class ListExpression(BaseModel):
    d: dict[str, tuple[str, str, float, bool]]  | None = None
