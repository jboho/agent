import warnings
import gradio as gr
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage, BaseMessage

from handlers.chat_model_start_handler import ChatModelStartHandler
from tools.sql import run_query_tool, describe_tables_tool
from tools.report import write_report_tool
from prompts.prompt_sql import prompt, memory

warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

handler = ChatModelStartHandler()

chat = ChatOpenAI(
    model_name="gpt-4o",
    callbacks=[handler]
)

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
    tools=tools,
    memory=memory
)

def convert_memory_to_chatbot_format(messages: list[BaseMessage]) -> list[dict]:
    gr_messages = []
    for m in messages:
        if m.type == "system":
            continue  # optional: skip system messages
        role = "user" if m.type == "human" else "assistant"
        gr_messages.append({"role": role, "content": m.content})
    return gr_messages

def converse(user_input, _):
    _ = agent_executor.run(user_input)
    updated_history = memory.load_memory_variables({})["chat_history"]
    chatbot_history = convert_memory_to_chatbot_format(updated_history)
    return "", chatbot_history

with gr.Blocks() as demo:
    gr.Markdown("## SQL + ChatGPT Agent")

    chatbot = gr.Chatbot(label="Chat History", type="messages")
    msg = gr.Textbox(placeholder="Ask a question...", lines=1, label="Query")

    msg.submit(fn=converse, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()
