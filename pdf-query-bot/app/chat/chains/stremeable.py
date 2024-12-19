from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler

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