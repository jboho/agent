from models.base_model import BaseModel
from langchain.chat_models import ChatAnthropic
from langchain.schema import BaseMessage
import os

class ClaudeModel(BaseModel):
    def __init__(self):
        self.llm = ChatAnthropic(
            model_name="claude-2",
            temperature=0,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate(self, prompt: list[BaseMessage]) -> str:
        return self.llm(prompt).content