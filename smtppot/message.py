import re, email, datetime, hashlib, os

class Message:
    url_regex = re.compile('https?://(?:[a-zA-Z]|[\d]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    def __init__(self, message):
        self.__raw_message = message
        self.__bodies = self.__attachments = None
        self.__urls = None
    
    def __try_extract_urls(self):
        if self.__urls is not None:
            self.__extract_urls()
        urls = map(lambda i: Message.url_regex.findall(i.content()), self.bodies())
        self.__urls = reduce(lambda x,y: x + y, urls)
    
    def __try_extract_body_and_attachments(self):
        if self.__bodies is not None:
            return
        bodies = []
        attachments = []
        message = self.__raw_message
        content = message.get_payload()
        if message.is_multipart():
            for mail in content:
                disposition = mail['Content-Disposition']
                if disposition and disposition.startswith('attachment'):
                    attachments.append(Attachment(mail))
                else:
                    bodies.append(MessageBody(mail))
        else:
            bodies.append(
                MessageBody(
                    email.message_from_string(
                        message.get_payload()
                    )
                )
            )
        self.__bodies = bodies
        self.__attachments = attachments
    
    def attachments(self):
        self.__try_extract_body_and_attachments()
        return self.__attachments
    
    def bodies(self):
        self.__try_extract_body_and_attachments()
        return self.__bodies
    
    def headers(self):
        return self.__raw_message.items()
    
    def urls(self):
        self.__try_extract_urls()
        return self.__urls
    
    def __str__(self):
        return str(self.__raw_message)
    
    def __try_create_dirs(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)
    
    def save_to_path(self, base_path):
        if not os.path.isdir(base_path):
            raise Exception("Base path does not exist.")
        now = datetime.datetime.now().date()
        path = os.path.join(base_path, str(now.year), str(now.month), str(now.day))
        self.__try_create_dirs(path)
        data = str(self)
        file_name = hashlib.sha1(data).hexdigest()
        fd = open(os.path.join(path, file_name), 'w')
        fd.write(data)
        fd.close()


class MessagePart:
    def __init__(self, message):
        payload = message.get_payload()
        # There shouldn't be a multipart message at this point
        if message.is_multipart():
            payload = payload[0]
        content_encoding = message['Content-Transfer-Encoding']
        if content_encoding == 'base64':
            payload = payload.decode('base64')
        self.__content = payload
        self.__headers = message.items()
    
    def content(self):
        return self.__content
    
    def headers(self):
        return self.__headers


class MessageBody(MessagePart):
    def __init__(self, part):
        MessagePart.__init__(self, part)


class Attachment(MessagePart):
    def __init__(self, attachment):
        disposition = attachment['Content-Disposition']
        result = re.findall('filename="([^"]+)', disposition)
        self.__name = result[0] if any(result) else ''
        MessagePart.__init__(
            self,
            attachment
        )
    
    def name(self):
        return self.__name
