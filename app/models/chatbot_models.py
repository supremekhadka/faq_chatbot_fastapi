from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class AnswerResponse(BaseModel):
    matched_question: Optional[str] = None
    answer: Optional[str] = None
    score: Optional[float] = None
    message: Optional[str] = None
