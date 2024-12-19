# Test file to lean how to extend the langchain library to support streaming

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
    
    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)
        
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
        
    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)

chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}"),
    
])

class StremeableChain:
    def stream(self, input, **kwargs):
        queue = Queue()
        hanlder = StreamingHandler(queue)
        
        def task():
            self(input, callbacks=[hanlder])
            
        Thread(target=task).start()
            
        while True:
            token = queue.get()
            if token is None:
                break
            yield token
        
class StreamingChain(StremeableChain, LLMChain):
    pass

chain = StreamingChain(
    llm=chat,
    prompt=prompt,
)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)