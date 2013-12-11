#!/usr/bin/python

from multiprocessing import Queue, Process
from smtppot import Consumer, HookManager, Server
import asyncore
import signal, time
import traceback
import config

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

def load_credentials(creds_path):
    """
    The credentials file format should be:
    user1:password1
    user2:password2
    
    This method returns a list of tuples:
    [ (user1, password1), (user2, password2), ...]
    """
    fd = open(creds_path)
    credentials = []
    for line in fd:
        # Remove the trailing \n and split the string by ':'
        data = line[:-1].split(':', 1)
        if len(data) == 2:
            credentials.append(tuple(data))
    return credentials

credentials = None

if config.credentials_file:
    try:
        credentials = load_credentials(config.credentials_file)
    except Exception as ex:
        print "Error opening credentials file: " + str(ex)
        exit(1)

queue = Queue()
srv = Server(
    credentials, 
    (config.bind_address, config.bind_port), 
    queue, 
    config.served_domain,
    server_banner=config.server_banner
)
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
