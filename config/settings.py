from pydantic import BaseModel, Field


class MiningSettings(BaseModel):
    min_support: int = Field(default=2, ge=1)
    max_pattern_length: int = Field(default=5, ge=1)


class LLMSettings(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4.1-mini"


class AppSettings(BaseModel):
    mining: MiningSettings = Field(default_factory=MiningSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
