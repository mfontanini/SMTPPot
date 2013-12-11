# This code has been taken from https://github.com/bcoe/secure-smtpd/
# and modified a little
import ssl, smtpd, asyncore, socket, logging

from smtp_channel import SMTPChannel
from asyncore import ExitNow
from process_pool import ProcessPool
from Queue import Empty
from ssl import SSLError

class SMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, banner="", credential_validator=None):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.credential_validator = credential_validator
        smtpd.__version__ = banner
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            newsocket, fromaddr = pair
            channel = SMTPChannel(
                self,
                newsocket,
                fromaddr,
                require_authentication=False,
                credential_validator=self.credential_validator
            )
