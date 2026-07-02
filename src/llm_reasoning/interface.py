from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def reason(self, prompt: str) -> str:
        raise NotImplementedError


class OpenAILLMClient(LLMClient):
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def reason(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text


class LocalLLMClient(LLMClient):
    def reason(self, prompt: str) -> str:
        raise NotImplementedError("Plug in a local LLM backend here.")
