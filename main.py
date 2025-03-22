# Using agents to run ChatGPT functions
import warnings
import gradio as gr
import anthropic

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler
# suppress deprecation warning for now
warnings.filterwarnings("ignore", category=DeprecationWarning)

# program starts
load_dotenv()

handler = ChatModelStartHandler()

chat = ChatOpenAI(
    model_name="gpt-4o",
    callbacks=[handler]
)

tables = list_tables()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQL database. \n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead use the 'describe_tables' function."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")

    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [
    run_query_tool, 
    describe_tables_tool, 
    write_report_tool
]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    # verbose=True,
    tools=tools,
    memory=memory
)

# console way to do this:
# while True:
#     chat_query = input("What would you like to ask? ")
#     response=agent_executor(chat_query)
#     print("\n")
#     print(response['output'])
#     print("\n")

def converse(user_input, history):
    # 1) Send user_input to the agent
    agent_response = agent_executor.run(user_input)
    
    # 2) Append messages in the "role-content" format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": str(agent_response)})
    
    # 3) Return a blank string for the input box and the updated list of messages
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("## SQL + ChatGPT Agent")

    # Chatbot with messages format
    chatbot = gr.Chatbot(type="messages", label="Chat History")

    msg = gr.Textbox(placeholder="Ask a question...")
    # On submit, call converse(...) with both the user message and entire history
    msg.submit(fn=converse, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()