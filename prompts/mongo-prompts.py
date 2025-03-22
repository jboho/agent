from langchain.prompts import PromptTemplate
from typing import List
from prompts.shared_prompt_utils import format_history_block

_mongo_template = """
You are an expert MongoDB agent.

Example:
User: Find all documents in users.
Mongo: db.users.find({})

{history_block}
User: {user_input}
Mongo:
"""

mongo_prompt = PromptTemplate(
    input_variables=["user_input", "history_block"],
    template=_mongo_template.strip()
)

def get_mongo_prompt(user_input: str, history: List[str] = None) -> str:
    history_block = format_history_block(history, "Mongo") if history else ""
    return mongo_prompt.format(user_input=user_input, history_block=history_block)
