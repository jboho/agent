from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from tools.sql import list_tables
from typing import Any

TABLES = list_tables()

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "You are an AI that has access to a SQL database. "
        f"The database has tables: {TABLES}. "
        "Do not make assumptions about what tables or columns exist. "
        "Use the 'describe_tables' function when needed."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

def get_sql_prompt() -> ChatPromptTemplate:
    return chat_prompt