from typing import List
from pydantic import BaseModel # type: ignore

class ExpressionRequset(BaseModel):
    expression: str

class ExpressionsResponse(BaseModel):
    task_id: str

class Expression(BaseModel):
    task_id: str
    expression: str
    result: float
    have_error: bool
    text_error: str

class ListExpression(BaseModel):
    expressions: List[Expression]
