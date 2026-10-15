import json
import os
import logging

logger = logging.getLogger(__name__)

from ollama import Client

from app.providers.base import LLMProvider

from app.tools.tool_registry import (
    TOOL_FUNCTIONS,
    get_ollama_tools,
)


class OllamaProvider(LLMProvider):

    def __init__(self):

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "qwen3:4b",
        )

        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        )

        self.client = Client(
            host=self.base_url
        )

        self.tools = get_ollama_tools()
        
        logger.info(
            "OllamaProvider inicializado. model=%s base_url=%s",
            self.model,
            self.base_url,
        )

    def chat(
        self,
        message: str,
        instructions: str,
    ) -> str:

        logger.info(
            "Iniciando requisição ao Ollama. model=%s",
            self.model,
        )

        logger.debug(
            "Mensagem recebida: %s",
            message,
        )

        messages = [
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        for iteration in range(5):

            logger.debug(
                "Iteração Ollama: %s",
                iteration + 1,
            )
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                tools=self.tools,
                stream=False,
            )

            assistant_message = response.message

            messages.append(
                assistant_message
            )

            tool_calls = (
                assistant_message.tool_calls or []
            )

            logger.debug(
                "Resposta recebida. tool_calls=%s",
                len(tool_calls),
            )

            if not tool_calls:

                logger.info(
                    "Ollama retornou resposta final."
                )

                return (
                    assistant_message.content
                    or "Não foi possível gerar uma resposta."
                )

            for call in tool_calls:

                function_name = (
                    call.function.name
                )

                arguments = (
                    call.function.arguments
                )

                # LOG 1: qual ferramenta o LLM escolheu
                logger.info(
                    "Ollama solicitou ferramenta: %s",
                    function_name,
                )

                # LOG 2: argumentos gerados pelo LLM
                logger.debug(
                    "Argumentos da ferramenta %s: %s",
                    function_name,
                    arguments,
                )

                function = TOOL_FUNCTIONS.get(
                    function_name
                )

                if function is None:

                    logger.warning(
                        "Ferramenta desconhecida: %s",
                        function_name,
                    )

                    result = {
                        "error": (
                            f"Ferramenta desconhecida: "
                            f"{function_name}"
                        )
                    }

                else:

                    try:

                        if isinstance(arguments, str):
                            arguments = json.loads(
                                arguments
                            )

                        result = function(
                            **arguments
                        )
                        
                        # LOG 3: ferramenta executada
                        logger.info(
                            "Ferramenta executada com sucesso: %s",
                            function_name,
                        )

                        # LOG 4: resultado retornado pela tool
                        logger.debug(
                            "Resultado de %s: %s",
                            function_name,
                            result,
                        )

                    except Exception as exc:

                        logger.exception(
                            "Erro ao executar ferramenta: %s",
                            function_name,
                        )

                        result = {
                            "error": str(exc)
                        }

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": function_name,
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                            default=str,
                        ),
                    }
                )

        logger.warning(
            "Limite de iterações do Ollama atingido."
        )

        return (
            "Não foi possível concluir a solicitação "
            "após várias tentativas."
        )