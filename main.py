import warnings
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from tools.sql import run_query_tool, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler
from prompts.sql_prompts import get_sql_prompt

# suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(model_name="gpt-4", callbacks=[handler])
prompt = get_sql_prompt(input="{input}", history=[])
tools = [run_query_tool, describe_tables_tool, write_report_tool]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

if __name__ == "__main__":
    while True:
        user_input = input("\nAsk a question: ")
        response = agent_executor.run(user_input)
        print("\n", response, "\n")
