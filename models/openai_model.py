from models.base_model import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

class OpenAIModel(BaseModel):
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(self, prompt: str) -> str:
        return self.llm([HumanMessage(content=prompt)]).content
