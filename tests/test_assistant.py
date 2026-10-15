from app.assistant import CalendarAssistant
from app.providers.base import LLMProvider


class FakeLLMProvider(LLMProvider):

    def __init__(self):
        self.received_message = None
        self.received_instructions = None

    def chat(
        self,
        message: str,
        instructions: str,
    ) -> str:

        self.received_message = message
        self.received_instructions = instructions

        return "Resposta simulada"


def test_assistant_with_fake_provider():

    provider = FakeLLMProvider()

    assistant = CalendarAssistant(
        llm_provider=provider
    )

    response = assistant.chat(
        "Quais são meus compromissos amanhã?"
    )

    assert response == "Resposta simulada"


def test_assistant_sends_message_to_provider():

    provider = FakeLLMProvider()

    assistant = CalendarAssistant(
        llm_provider=provider
    )

    assistant.chat(
        "Estou livre amanhã às 14h?"
    )

    assert (
        provider.received_message
        == "Estou livre amanhã às 14h?"
    )


def test_assistant_sends_calendar_instructions():

    provider = FakeLLMProvider()

    assistant = CalendarAssistant(
        llm_provider=provider
    )

    assistant.chat(
        "O que tenho amanhã?"
    )

    instructions = provider.received_instructions

    assert "Google Calendar" in instructions
    assert "America/Sao_Paulo" in instructions
    assert "Nunca inventar compromissos" in instructions