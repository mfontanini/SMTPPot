from secure_smtpd import SMTPServer, CredentialsValidator
import asyncore


class Server(SMTPServer):
    def __init__(self, credentials):
        self.__credentials_validator = CredentialsValidator(credentials)
        SMTPServer.__init__(
            self,
            ('localhost', 1337),
            None,
            credential_validator=self.__credentials_validator
        )

    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Mensaje llego!'
    
    def run(self):
        asyncore.loop()
        

credentials = [
    ('user', 'pass')
]
srv = Server(credentials)
srv.run()
