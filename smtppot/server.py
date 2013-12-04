from secure_smtpd import SMTPServer, CredentialsValidator
import asyncore, time, re


class Server(SMTPServer):
    def __init__(self, credentials, queue, handled_domain='', open_relay=False):
        self.__credentials_validator = CredentialsValidator(credentials)
        self.__domain = handled_domain
        self.__queue = queue
        self.__open_relay = open_relay
        SMTPServer.__init__(
            self,
            ('localhost', 1337),
            None,
            credential_validator=self.__credentials_validator,
            process_count=1
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
        self.__queue.put(data)
    
    def run(self):
        asyncore.loop()
        
