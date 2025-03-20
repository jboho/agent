import os
import psycopg2
from psycopg2 import sql
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool
from dotenv import load_dotenv

# Check if .env file exists before loading
if not os.path.exists(".env"):
    print("Warning: .env file not found! Make sure to create it from .env.example and set your database credentials.")

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Ensure all required environment variables are set
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise EnvironmentError("Missing required database environment variables. Check your .env file.")

# Establish PostgreSQL connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def list_tables():
    """List all tables in the PostgreSQL database."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        rows = cur.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_postgres_query(query):
    """Execute a PostgreSQL query and return results."""
    with conn.cursor() as cur:
        try:
            cur.execute(query)
            if query.strip().lower().startswith("select"):
                return cur.fetchall()
            conn.commit()
            return "Query executed successfully."
        except psycopg2.Error as err:
            return f"The following error occurred: {str(err)}"

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_postgres_query",
    description="Run a PostgreSQL query.",
    func=run_postgres_query,
    args_schema=RunQueryArgsSchema
)

def describe_tables(table_names):
    """Get the schema of the given tables."""
    tables = ', '.join(f"'{table}'" for table in table_names)
    query = f"""
        SELECT table_name, column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name IN ({tables});
    """
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    
    return "\n".join(f"Table: {row[0]}, Column: {row[1]}, Type: {row[2]}" for row in rows)

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
