#!/usr/bin/python

from multiprocessing import Queue, Process
from smtppot import Consumer
from smtppot import Server
import asyncore
import signal, time


def run_consumer(queue):
    try:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        consumer = Consumer(queue)
        consumer.process()
    except Exception as ex:
        pass

credentials = [
    ('user', 'pass')
]
queue = Queue()
srv = Server(credentials, ('localhost', 1337), queue, "mail.example.com")
consumer_proc = Process(target=run_consumer, args=(queue, ))
consumer_proc.start()

signal.signal(signal.SIGINT, lambda x,y: asyncore.close_all())
try:
    asyncore.loop()
except Exception as ex:
    pass
queue.put(None)
consumer_proc.join()
