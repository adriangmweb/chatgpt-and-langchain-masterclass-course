from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from redundant_filter_retriever import RedundantFilterRetriever
import os
import langchain

langchain.debug = True

load_dotenv()

chat = ChatOpenAI()

embeddings = OpenAIEmbeddings()

current_dir = os.path.dirname(os.path.abspath(__file__))

vector_store = Chroma(
    persist_directory=current_dir + "/embeddings",
    embedding_function=embeddings
)

retriever = RedundantFilterRetriever(
    embeddings=embeddings,
    chroma=vector_store
)

chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type="stuff",
    retriever=retriever
)

result = chain.run("What is an interesting fact about the the english language?")

print(result)
