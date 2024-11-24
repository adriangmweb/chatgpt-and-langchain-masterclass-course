from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
load_dotenv()


chat = ChatOpenAI()

tables = list_tables()
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            f"You are a helpful assistant that can answer questions about a SQLite database with the following tables: {tables}."
            "Do not make any assumptions about what tables or columns exist. Instead, use the `describe_tables` tool to learn about the tables."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
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
    verbose=True,
    memory=memory
)

agent_executor("Summarize the top 5 most popular products and write an HTML report of the results")
agent_executor("Do the same with the top 5 most popular categories")
