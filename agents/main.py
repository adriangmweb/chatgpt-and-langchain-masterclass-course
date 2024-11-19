from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from dotenv import load_dotenv

from tools.sql import run_query_tool

load_dotenv()


chat = ChatOpenAI()
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [run_query_tool]

agent = OpenAIFunctionsAgent(
    llm=chat, 
    prompt=prompt, 
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

agent_executor("How many users are in the database?")