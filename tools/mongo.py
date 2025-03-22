from pymongo import MongoClient
import os

class MongoConnector:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = db_name or os.getenv("MONGO_DB", "test")
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def list_collections(self):
        return self.db.list_collection_names()

    def get_sample_document(self, collection_name):
        return self.db[collection_name].find_one() or {}

    def describe_collections(self):
        schema = {}
        for col in self.list_collections():
            sample = self.get_sample_document(col)
            schema[col] = list(sample.keys()) if sample else []
        return schema

    def run_query(self, collection_name, query: dict):
        try:
            cursor = self.db[collection_name].find(query)
            return list(cursor)
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    mongo = MongoConnector()
    print("Collections:", mongo.list_collections())
    print("Schema:", mongo.describe_collections())
