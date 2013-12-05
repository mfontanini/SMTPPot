from secure_smtpd import SMTPServer, CredentialsValidator
import asyncore, time, re
from multiprocessing import Process


class Server(SMTPServer):
    def __init__(self, credentials, bind_pair, queue, handled_domain='', open_relay=False):
        self.__credentials_validator = CredentialsValidator(credentials)
        self.__domain = handled_domain
        self.__queue = queue
        self.__open_relay = open_relay
        SMTPServer.__init__(
            self,
            bind_pair,
            None,
            credential_validator=self.__credentials_validator
        )

    def __extract_domain(self, mail):
        matches = re.findall('@(.*)', mail)
        return matches[0] if any(matches) else ''

    def process_message(self, peer, mailfrom, rcpttos, data, auth_data):
        if not self.__open_relay:
            domains = map(self.__extract_domain, rcpttos)
            extern_domains = filter(lambda i: i != self.__domain, domains)
            if any(extern_domains) and auth_data is None:
                return "530 Authentication required"
        extra_headers = [
            'X-Client-IP: ' + peer[0],
            'X-RCPT-To: ' + ','.join(rcpttos)
        ]
        if auth_data:
            extra_headers.append('X-Authenticated-Username: ' + auth_data[0])
        extra_headers.append('')
        self.__queue.put('\r\n'.join(extra_headers) + data)
    
    def __do_run(self):
        asyncore.loop()
    
    def run(self):
        p = Process(target=self.__do_run)
        p.run()
        
