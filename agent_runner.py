from models.openai_model import OpenAIModel
from models.claude_model import ClaudeModel
from prompts.sql_prompts import get_sql_prompt
from prompts.mongo_prompts import get_mongo_prompt
from agents.sql_agent import SQLAgent
from agents.mongo_agent import MongoAgent

MODEL_REGISTRY = {
    "openai": OpenAIModel,
    "claude": ClaudeModel,
}

AGENT_REGISTRY = {
    "sql": SQLAgent,
    "mongo": MongoAgent,
}

def run_agent():
    agent_type = "sql"      # "mongo" also supported
    model_type = "openai"   # or "claude"

    model = MODEL_REGISTRY[model_type]()
    agent = AGENT_REGISTRY[agent_type](model)

    history = [
        "List all employees in the HR department.",
        "Show the total revenue per region.",
    ]

    user_input = "Get all customers from Germany."

    if agent_type == "sql":
        prompt = get_sql_prompt(user_input, history)
    else:
        prompt = get_mongo_prompt(user_input, history)

    print("--- FORMATTED PROMPT ---")
    print(prompt)

    result = agent.run(prompt)
    print("--- MODEL RESPONSE ---")
    print(result)
