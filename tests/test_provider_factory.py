from app.providers.ollama_provider import (
    OllamaProvider,
)

from app.providers.factory import (
    create_llm_provider,
)


def test_factory_creates_ollama_provider(
    monkeypatch,
):

    monkeypatch.setenv(
        "LLM_PROVIDER",
        "ollama",
    )

    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "qwen3:4b",
    )

    provider = create_llm_provider()

    assert isinstance(
        provider,
        OllamaProvider,
    )

    assert provider.model == "qwen3:4b"