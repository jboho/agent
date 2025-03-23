# File: prompts/sql_prompts.py
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from typing import List
from tools.sql import describe_tables, list_tables

SQL_SYSTEM_PROMPT = """
You are an expert SQL agent tasked with generating SQL queries based on a user's request.

The database has the following schema:
{schema}

Only return the raw SQL query — do not add any explanations, markdown, or formatting. Return a single SQL statement ending in a semicolon.
""".strip()

FORMATTER_SYSTEM_PROMPT = """
You are a helpful assistant that formats SQL query results into friendly, natural language responses.

When given a SQL query and its result:
1. If it's a single number, boolean, or short string — summarize it naturally and conversationally.
2. If it's a list of rows, format it into a clean, markdown-style table.

Respond in a clear, polite, and human tone.
""".strip()

def get_sql_prompt(user_input: str, history: List[str] = None, schema: str = "") -> List[BaseMessage]:
    messages: List[BaseMessage] = []

    messages.append(SystemMessage(
        content=SQL_SYSTEM_PROMPT.format(schema=schema.strip())
    ))

    if history:
        for user_msg in history:
            messages.append(HumanMessage(content=user_msg))
            messages.append(AIMessage(content="..."))

    messages.append(HumanMessage(content=user_input))
    return messages

def build_sql_prompt(user_input: str, history: List[str]) -> List[BaseMessage]:
    table_names = list_tables().split("\n")
    schema = describe_tables(table_names)
    return get_sql_prompt(user_input, history, schema)

def get_formatter_prompt(result: str) -> List[BaseMessage]:
    return [
        SystemMessage(content=FORMATTER_SYSTEM_PROMPT),
        HumanMessage(content=f"Format this SQL result: {result}")
    ]
