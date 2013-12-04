#!/usr/bin/python

from multiprocessing import Queue
from smtppot import Consumer
from smtppot import Server

credentials = [
    ('user', 'pass')
]
q = Queue()
c = Consumer(q)
srv = Server(credentials, q, "mail.example.com")
c.start()
try:
    srv.run()
except:
    pass
c.stop()
