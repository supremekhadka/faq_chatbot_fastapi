import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.faq_service import FAQService

pytestmark = pytest.mark.asyncio

app.state.faq_service = FAQService()


async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FAQ Chatbot API"}


async def test_ask_question_valid():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/query", json={"query": "What are your hours?"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data or "message" in data


async def test_ask_question_empty_query():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/api/v1/query", json={"query": " "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Query cannot be empty."}


async def test_ask_question_no_match():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/query", json={"query": "What is the meaning of life?"}
        )
    assert response.status_code == 200
    data = response.json()
    assert (
        data["message"] == "Sorry, I couldn't find a relevant answer to your question."
        or data["answer"] is not None
    )
