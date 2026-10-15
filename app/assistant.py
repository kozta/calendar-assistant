from datetime import datetime
from zoneinfo import ZoneInfo

from app.providers.base import LLMProvider


TIMEZONE = ZoneInfo(
    "America/Sao_Paulo"
)


class CalendarAssistant:

    def __init__(
        self,
        llm_provider: LLMProvider,
    ):
        self.llm_provider = llm_provider

    def chat(
        self,
        message: str,
    ) -> str:

        now = datetime.now(
            TIMEZONE
        )

        instructions = f"""
        Você é um assistente pessoal especializado
        em Google Calendar.

        Data e hora atual:
        {now.isoformat()}

        Timezone:
        America/Sao_Paulo

        Suas responsabilidades:

        1. Consultar eventos.
        2. Verificar disponibilidade.
        3. Responder em português.
        4. Interpretar datas relativas.
        5. Nunca inventar compromissos.
        6. Utilizar ferramentas para consultar
           a agenda.

        Quando o usuário perguntar sobre amanhã,
        calcule a data considerando a data atual.

        Se não houver duração informada para uma
        consulta de disponibilidade, considere
        1 hora.

        Não crie, altere ou exclua eventos.
        """

        return self.llm_provider.chat(
            message=message,
            instructions=instructions,
        )