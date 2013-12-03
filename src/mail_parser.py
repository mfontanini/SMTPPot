import email, timeit
from message import Message, Attachment

class MailParser:
    def __init__(self):
        pass

    def __do_parse(self, msg):
        message = Message(msg)
        for a in message.urls():
            print a
        return message

    def parse_string(self, data):
        msg = email.message_from_string(data)
        return self.__do_parse(msg)

fd = open('/tmp/url')
data = fd.read()
x = MailParser()
x.parse_string(data)
#print timeit.timeit("MailParser().parse_string(data)", "from __main__ import MailParser, data", number=5000)
