from langchain.prompts import PromptTemplate
from typing import List
from prompts.shared_prompt_utils import format_history_block

_sql_template = """
You are an expert SQL agent.

Example:
User: Show all users.
SQL: SELECT * FROM users;

{history_block}
User: {user_input}
SQL:
"""

sql_prompt = PromptTemplate(
    input_variables=["user_input", "history_block"],
    template=_sql_template.strip()
)

def get_sql_prompt(user_input: str, history: List[str] = None) -> str:
    history_block = format_history_block(history, "SQL") if history else ""
    return sql_prompt.format(user_input=user_input, history_block=history_block)
