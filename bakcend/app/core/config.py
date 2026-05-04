"""
Global configuration settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

#? BaseSettings is a Pydantic model that reads from environment variables
# automatically. In TS, we'd use zod to validate the environment variables:
# const config = z.object({ DATABASE_URL: z.string() }).parse(process.env)

class Settings(BaseSettings):
    # model_config tells Pydantic where to read env vars from
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False, # DATABASE_URL == database_url
        extra="ignore" # Ignore unknown env vars
    )

    # App
    app_name: str = "AI Chatbot"
    app_version: str = "0.1.0"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = Field(
        default="postgresql+psycopg://user:password@localhost:5432/chatbot"
    )

    # LLM API Keys
    openai_api_key: str | None = None
    gemini_api_key: str | None = None

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma4"

    # Scraper
    target_url: str = "https://www.amazon.de"
    max_scrape_pages: int = 5

    # Embedding model
    embedding_model: str = "text-embedding-3-small" #* OpenAI default, Or we can use "gemini-embedding-001" for Gemini

#? Singleton pattern - one instance shared across the whole app
# In TS, we'd use export const config = new Settings()
settings = Settings()