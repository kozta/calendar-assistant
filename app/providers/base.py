from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def chat(
        self,
        message: str,
        instructions: str,
    ) -> str:
        pass