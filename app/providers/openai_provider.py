import json
import os

from openai import OpenAI

from app.providers.base import LLMProvider
from app.tools.tool_registry import (
    TOOLS,
    TOOL_FUNCTIONS,
)


class OpenAIProvider(LLMProvider):

    def __init__(self):
        self.client = OpenAI()

        self.model = os.getenv(
            "OPENAI_MODEL"
        )

        if not self.model:
            raise ValueError(
                "OPENAI_MODEL não configurado."
            )

    def chat(
        self,
        message: str,
        instructions: str,
    ) -> str:

        input_messages = [
            {
                "role": "user",
                "content": message,
            }
        ]

        for _ in range(5):

            response = self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=input_messages,
                tools=TOOLS,
            )

            input_messages.extend(
                response.output
            )

            function_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                return response.output_text

            for call in function_calls:

                function = TOOL_FUNCTIONS.get(
                    call.name
                )

                if function is None:

                    result = {
                        "error": (
                            f"Ferramenta desconhecida: "
                            f"{call.name}"
                        )
                    }

                else:

                    try:

                        arguments = json.loads(
                            call.arguments
                        )

                        result = function(
                            **arguments
                        )

                    except Exception as exc:

                        result = {
                            "error": str(exc)
                        }

                input_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(
                            result,
                            ensure_ascii=False,
                            default=str,
                        ),
                    }
                )

        return (
            "Não foi possível concluir "
            "a solicitação."
        )