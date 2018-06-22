from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class Conversation:
    title = ""
    messages = []

    def set_conversation(self, title="", messages=[]):
        self.title = title
        self.messages = messages

    def display(self):
        GenLogger.info(self.title)
        for msg in self.messages:
            GenLogger.info(msg.content)


class Message:
    time = ""
    content = ""
    msg_type = ""

    def set_message(self, time="", content="", msg_type=""):
        self.time = time
        self.content = content
        self.msg_type = msg_type

    def display(self):
        GenLogger.info(self.time + " <<>> " + self.content + " <<>> " + self.msg_type)


class Post:

    id = ""
    title = ""
    text = ""
    images = []

    def display(self):
        GenLogger.info(self.id)
        GenLogger.info(self.title)
        GenLogger.info(self.text)
        for image in self.images:
            GenLogger.info(image)

    def set_post(self, identifier, title, images, text):
        self.id = identifier
        self.title = title
        self.text = text
        self.images = images


class Comment:
    iden = ""
    text = ""
    repliesList = []

    def set_comment(self, iden="", text=""):
        self.iden = iden
        self.text = text

    def display(self):
        GenLogger.info(self.iden + " <<>> " + self.text + " <<>> ")


class DOMContent:

    posts = []
    conversations = []

    def display(self):
        GenLogger.info("Posts..")
        for post in self.posts:
            GenLogger.info(post.text)
            GenLogger.info(post.images)
        GenLogger.info("Conversations..")
        for conversation in self.conversations:
            GenLogger.info(conversation.title)
            GenLogger.info(conversation.messages)

    def set_post(self, post=Post()):
        self.posts.append(post)

    def set_conversation(self, conversation=Conversation()):
        self.conversations.append(conversation)
