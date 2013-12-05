import email
from multiprocessing import Queue
from message import Message
from threading import Thread

class Consumer:
    def __init__(self, queue, hook_manager):
        # Consumer stuff
        self.__queue = queue
        self.__hook_manager = hook_manager
    
    def enqueue(self, mail):
        self.__queue.put(mail)
    
    def process(self):
        while True:
            data = self.__queue.get()
            # We push None when there's nothing left
            if data is None:
                return
            msg = email.message_from_string(data)
            msg = Message(msg)
            self.__hook_manager.run_hooks(msg)
