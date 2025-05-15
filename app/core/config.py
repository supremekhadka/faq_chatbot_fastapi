from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FAQ Chatbot API"
    API_V1_STR: str = "/api/v1"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD: float = 0.5
    LOG_LEVEL: str = "INFO"
    FAQ_FILE_PATH: str = "data/faqs.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
