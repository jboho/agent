# File: ui/gradio_ui.py
import gradio as gr
from models.openai_model import OpenAIModel
from models.claude_model import ClaudeModel
from prompts.sql_prompts import build_sql_prompt
from agents.sql_agent import SQLAgent
from tools.sql import describe_tables, list_tables

MODEL_REGISTRY = {
    "openai": OpenAIModel,
    "claude": ClaudeModel,
}

AGENT = SQLAgent

def converse(user_input, history, model_choice):
    messages = [msg["content"] for msg in history if msg["role"] == "user"]
    prompt = build_sql_prompt(user_input, messages)

    model = MODEL_REGISTRY[model_choice]()
    agent = AGENT(model)
    response = agent.run(prompt)

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
