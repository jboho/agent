from tools.sql import run_sqlite_query
from prompts.sql_prompts import get_formatter_prompt

class SQLAgent:
    def __init__(self, model):
        self.model = model

    def run(self, prompt: list) -> str:
        raw_query = self.model.generate(prompt).strip()

        try:
            result = run_sqlite_query(raw_query)
            formatted_prompt = get_formatter_prompt(str(result))
            formatted_output = self.model.generate(formatted_prompt)
            return formatted_output
        except Exception as e:
            return f"Error executing query: {e}"
