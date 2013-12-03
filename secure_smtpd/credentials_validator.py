class CredentialsValidator:
    def __init__(self, credentials):
        self.__credentials = set(credentials)
    
    def validate(self, username, password):
        return (username, password) in self.__credentials
