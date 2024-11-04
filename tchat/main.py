from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import FileChatMessageHistory, ConversationSummaryBufferMemory
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

memory = ConversationSummaryBufferMemory(
    chat_memory = FileChatMessageHistory("chat-memory.json"),
    memory_key="messages",
    llm=chat,
    return_messages=True
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

while True:
    content = input(">>: ")
    
    result = chain({"content": content})
    
    print(result["text"])