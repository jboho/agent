from models.base_model import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage
import os

class OpenAIModel(BaseModel):
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(self, prompt: list[BaseMessage]) -> str:
        return self.llm(prompt).content