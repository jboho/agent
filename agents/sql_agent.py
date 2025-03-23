from tools.sql import run_sqlite_query, list_tables

class SQLAgent:
    def __init__(self, model):
        self.model = model

    def run(self, prompt: str) -> str:
        query = self.model.generate(prompt)

        try:
            result = run_sqlite_query(query)
            return str(result)
        except Exception as e:
            return f"Error executing query: {e}"

    def list_tables(self) -> str:
        return list_tables()