from dotenv import load_dotenv

from app.providers.ollama_provider import (
    OllamaProvider,
)


load_dotenv()


def test_ollama_basic_chat():

    provider = OllamaProvider()

    response = provider.chat(
        message="Responda apenas OK.",
        instructions=(
            "Você é um assistente. "
            "Responda em português."
        ),
    )

    print("\nResposta Ollama:")
    print(response)

    assert isinstance(response, str)
    assert len(response.strip()) > 0