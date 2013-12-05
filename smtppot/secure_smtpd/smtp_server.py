# This code has been taken from https://github.com/bcoe/secure-smtpd/
# and modified a little
import ssl, smtpd, asyncore, socket, logging

from smtp_channel import SMTPChannel
from asyncore import ExitNow
from process_pool import ProcessPool
from Queue import Empty
from ssl import SSLError

class SMTPServer(smtpd.SMTPServer):
    
    def __init__(self, localaddr, remoteaddr, ssl=False, certfile=None, keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, require_authentication=False, credential_validator=None, maximum_execution_time=30, process_count=5):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.subprocesses = []
        self.require_authentication = require_authentication
        self.credential_validator = credential_validator
        self.ssl = ssl
        self.maximum_execution_time = maximum_execution_time
        self.process_count = process_count
        self.process_pool = None
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            newsocket, fromaddr = pair
            channel = SMTPChannel(
                self,
                newsocket,
                fromaddr,
                require_authentication=self.require_authentication,
                credential_validator=self.credential_validator
            )
