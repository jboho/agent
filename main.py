# File: main.py
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from prompts.sql_prompts import get_sql_prompt
from tools.sql import run_query_tool, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler
from models.claude_model import ClaudeModel

MODEL_REGISTRY = {
    "openai": lambda: ChatOpenAI(model_name="gpt-4"),
    "claude": lambda: ClaudeModel().llm,
}

def build_agent(model):
    prompt = get_sql_prompt()
    tools = [run_query_tool, describe_tables_tool, write_report_tool]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return AgentExecutor(
        agent=OpenAIFunctionsAgent(llm=model, prompt=prompt, tools=tools),
        tools=tools,
        memory=memory,
        verbose=False
    )

def converse(user_input, history, model_choice):
    model = MODEL_REGISTRY[model_choice]()
    agent_executor = build_agent(model)
    response = agent_executor.run({"input": user_input, "chat_history": history})

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
        msg = gr.Textbox(placeholder="Ask a question...", lines=1, label="Query")
    with gr.Row():
        clear_btn = gr.Button("Clear History")

    msg.submit(fn=converse, inputs=[msg, chatbot, model_choice], outputs=[msg, chatbot])
    clear_btn.click(fn=clear_history, outputs=[chatbot])

if __name__ == "__main__":
    demo.launch()
