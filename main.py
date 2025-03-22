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

def converse(user_input, history, model_choice):
    response = f"[{model_choice}] Response to: {user_input}"
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    return "", history

def clear_history():
    return []

with gr.Blocks() as demo:
    gr.Markdown("""
    # 💬 AI SQL Agent Playground
    Compare different models (ChatGPT-4, Claude) in a live chat interface.
    """)

    model_choice = gr.Radio(
        choices=["openai", "claude"],
        label="Select Model",
        value="openai",
        interactive=True
    )

    chatbot = gr.Chatbot(label="Chat History", type="messages")

    with gr.Row():
        msg = gr.Textbox(placeholder="Ask a question...", lines=1)
        clear_btn = gr.Button("Clear History")

    msg.submit(fn=converse, inputs=[msg, chatbot, model_choice], outputs=[msg, chatbot])
    clear_btn.click(fn=clear_history, outputs=[chatbot])

demo.launch()