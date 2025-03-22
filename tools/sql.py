import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

DB_PATH = "db.sqlite"

def list_tables():
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = c.fetchall()
        return "\n".join(row[0] for row in rows if row[0] is not None)
    finally:
        conn.close()

def run_sqlite_query(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"
    finally:
        conn.close()

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

def describe_tables(table_names: List[str]):
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        tables = ', '.join("'" + table + "'" for table in table_names)
        rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
        return "\n".join(row[0] for row in rows if row[0] is not None)
    finally:
        conn.close()

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
