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
        self.process_pool = ProcessPool(self._accept_subprocess, process_count=self.process_count)
        self.close()
    
    def _accept_subprocess(self, queue):
        while True:
            try:
                self.socket.setblocking(1)
                pair = self.accept()
                map = {}
                
                if pair is not None:
                    
                    newsocket, fromaddr = pair
                    newsocket.settimeout(self.maximum_execution_time)
                    
                    if self.ssl:
                        newsocket = ssl.wrap_socket(
                            newsocket,
                            server_side=True,
                            certfile=self.certfile,
                            keyfile=self.keyfile,
                            ssl_version=self.ssl_version,
                        )
                    channel = SMTPChannel(
                        self,
                        newsocket,
                        fromaddr,
                        require_authentication=self.require_authentication,
                        credential_validator=self.credential_validator,
                        map=map
                    )
                    asyncore.loop(map=map)
            except (ExitNow, SSLError):
                self._shutdown_socket(newsocket)
            except Exception, e:
                self._shutdown_socket(newsocket)
      
    def _shutdown_socket(self, s):
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception, e:
            pass
