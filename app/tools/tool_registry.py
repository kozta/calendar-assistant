from app.tools.calendar_tools import (list_calendar_events,check_calendar_availability,)


TOOLS = [
    {
        "type": "function",
        "name": "list_calendar_events",
        "description": "Lista eventos do Google Calendar em um período.",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "Data inicial ISO 8601 com timezone",
                },
                "end": {
                    "type": "string",
                    "description": "Data final ISO 8601 com timezone",
                },
            },
            "required": ["start", "end"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "check_calendar_availability",
        "description": "Verifica disponibilidade no Google Calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "Data inicial ISO 8601 com timezone",
                },
                "end": {
                    "type": "string",
                    "description": "Data final ISO 8601 com timezone",
                },
            },
            "required": ["start", "end"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


TOOL_FUNCTIONS = {
    "list_calendar_events": list_calendar_events,
    "check_calendar_availability": check_calendar_availability,
}

def get_ollama_tools() -> list[dict]:
    """
    Converte os schemas da OpenAI Responses API
    para o formato esperado pelo Ollama.
    """

    ollama_tools = []

    for tool in TOOLS:

        ollama_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
        )

    return ollama_tools