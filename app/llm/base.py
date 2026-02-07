from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generates a response from the LLM."""
        pass

    @abstractmethod
    def stream(self, prompt: str):
        """Streams a response from the LLM."""
        pass
