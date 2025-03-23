from tools.mongo import MongoConnector

class MongoAgent:
    def __init__(self, model):
        self.model = model
        self.db = MongoConnector()

    def run(self, prompt: str) -> str:
        query_text = self.model.generate(prompt)

        try:
            # Expect model to return something like: db.collection.find({...})
            exec_env = {}
            exec(f"result = {query_text}", {"db": self.db.db}, exec_env)
            result = exec_env.get("result")
            return str(result)
        except Exception as e:
            return f"Error running query: {e}"
