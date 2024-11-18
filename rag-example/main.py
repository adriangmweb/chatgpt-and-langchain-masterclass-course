import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

current_dir = os.path.dirname(os.path.abspath(__file__))
loader = TextLoader(current_dir + "/facts.txt")
docs = loader.load_and_split(text_splitter)

vector_store = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory=current_dir + "/embeddings"
)

results = vector_store.similarity_search(
    "What is an interesting fact about the the english language?",
    k=2 # get the top 2 results
)

for result in results:
    print("\n")
    print(result.page_content)
