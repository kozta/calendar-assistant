import os

from dotenv import load_dotenv

from app.providers.base import LLMProvider

from app.providers.openai_provider import (
    OpenAIProvider,
)

from app.providers.ollama_provider import (
    OllamaProvider,
)


load_dotenv()


def create_llm_provider() -> LLMProvider:

    provider = os.getenv(
        "LLM_PROVIDER",
        "openai",
    ).lower()

    if provider == "openai":

        return OpenAIProvider()

    if provider == "ollama":

        return OllamaProvider()

    raise ValueError(
        f"LLM provider não suportado: {provider}"
    )