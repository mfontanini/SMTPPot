#!/usr/bin/python

from multiprocessing import Queue, Process
from smtppot import Consumer, HookManager, Server
import asyncore
import signal, time
import traceback


def run_consumer(queue):
    try:
        hook_manager = HookManager()
        hook_manager.load_hooks("hooks")
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        consumer = Consumer(queue, hook_manager)
        consumer.process()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print traceback.format_exc()

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
except KeyboardInterrupt:
    pass
except Exception as ex:
    print traceback.format_exc()
queue.put(None)
consumer_proc.join()
