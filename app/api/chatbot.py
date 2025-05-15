from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.config import settings
from app.models.chatbot_models import AnswerResponse, QueryRequest
from app.services.faq_service import FAQService

router = APIRouter()

faq_service_instance = FAQService(model_name=settings.SENTENCE_TRANSFORMER_MODEL)


async def get_faq_service(request: Request) -> FAQService:
    return request.app.state.faq_service


@router.post("/query", response_model=AnswerResponse)
async def ask_question(
    request: QueryRequest, faq_service: FAQService = Depends(get_faq_service)
):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    result = faq_service_instance.get_best_answer(
        request.query, similarity_threshold=settings.SIMILARITY_THRESHOLD
    )

    if result:
        return AnswerResponse(
            matched_question=result["question"],
            answer=result["answer"],
            score=result["score"],
        )
    else:
        return AnswerResponse(
            message="Sorry, I couldn't find a relevant answer to your question."
        )
