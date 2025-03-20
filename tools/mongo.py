import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool
from dotenv import load_dotenv

# Check if .env file exists
if not os.path.exists(".env"):
    print("⚠️ Warning: .env file not found! Make sure to create it from .env.example and set your database credentials.")

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # Example: "mongodb://localhost:27017"
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  # Database name

# Ensure required environment variables are set
if not all([MONGO_URI, MONGO_DB_NAME]):
    raise EnvironmentError("❌ Missing MongoDB environment variables. Check your .env file.")

# Create a MongoDB client (connection pool is managed automatically)
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

async def list_collections():
    """List all collections (equivalent to SQL tables) in the MongoDB database."""
    collections = await db.list_collection_names()
    return "\n".join(collections)

async def run_mongo_query(collection_name: str, query: dict):
    """Execute a MongoDB query on a specific collection."""
    collection = db[collection_name]
    cursor = collection.find(query)  # Find documents matching the query
    documents = await cursor.to_list(length=100)  # Limit to 100 results
    return documents

class RunQueryArgsSchema(BaseModel):
    collection_name: str
    query: dict

run_query_tool = Tool.from_function(
    name="run_mongo_query",
    description="Run a MongoDB query using an async connection pool.",
    func=run_mongo_query,
    args_schema=RunQueryArgsSchema
)

async def describe_collections(collection_names: List[str]):
    """Describe the schema of given collections (returns sample documents)."""
    descriptions = []
    for collection_name in collection_names:
        collection = db[collection_name]
        sample_doc = await collection.find_one()  # Get one sample document
        descriptions.append(f"Collection: {collection_name}, Sample Schema: {sample_doc}")
    return "\n".join(descriptions)

class DescribeCollectionsArgsSchema(BaseModel):
    collection_names: List[str]

describe_collections_tool = Tool.from_function(
    name="describe_collections",
    description="Given a list of collection names, return sample document schemas.",
    func=describe_collections,
    args_schema=DescribeCollectionsArgsSchema
)

async def close_mongo_connection():
    """Close the MongoDB connection."""
    client.close()
    print("🔌 MongoDB connection closed.")
