from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI

from app.api import chatbot
from app.core.config import settings
from app.services.faq_service import FAQService

faq_service_global: Optional[FAQService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading FAQ service and model...")
    app.state.faq_service = FAQService(model_name=settings.SENTENCE_TRANSFORMER_MODEL)
    print("FAQ service loaded.")
    yield
    print("Shutting down...")
    app.state.faq_service = None


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(chatbot.router, prefix=settings.API_V1_STR, tags=["chatbot"])


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}
