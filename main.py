# Using agents to run ChatGPT functions
import warnings
import gradio as gr
# import anthropic

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


# while True:
#     chat_query = input("What would you like to ask? ")
#     response=agent_executor(chat_query)
#     print("\n")
#     print(response['output'])
#     print("\n")


def converse(user_input, history):
    """
    user_input: Latest message from user
    history: List of (user_msg, bot_msg) tuples
    """
    # Run the agent against the user query
    result = agent_executor.run(user_input)
    # Add (user_input, result) to history so the chatbot can display it
    history.append((user_input, result))
    # Return a blank string for the input box, and updated history
    return "", history


with gr.Blocks() as demo:
    gr.Markdown("## SQL + ChatGPT Agent")

    # By specifying `type="messages"`, Gradio will use the message dictionary format
    chatbot = gr.Chatbot(type="messages", label="Chat History")

    # Textbox for user to submit queries
    msg = gr.Textbox(
        placeholder="Ask something about the SQL database..."
    )

    # Submitting text calls 'converse' and updates the Chatbot
    msg.submit(
        fn=converse,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

demo.launch()



# # Build a Gradio UI with Blocks
# with gr.Blocks() as demo:
#     gr.Markdown("## SQL + ChatGPT Agent\nEnter your query below:")
    
#     chatbot = gr.Chatbot()  
#     msg = gr.Textbox(placeholder="Ask about the SQL database here...")

#     # Each time the user submits text, we run 'converse'
#     # Inputs: the new message + the entire chat history
#     # Outputs: reset the message box and update the chat history
#     msg.submit(converse, inputs=[msg, chatbot], outputs=[msg, chatbot])

# # Launch the Gradio app
# demo.launch()
