class RawMessage:
    def __init__(self, content, peer):
        self.__content = content
        self.__peer = peer
    
    def content(self):
        return self.__content
    
    def content_length(self):
        return len(self.__content)
