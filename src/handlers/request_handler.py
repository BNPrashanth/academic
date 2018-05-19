from dom_handler import DOM
from utilities.util_classes import DOMContent
from chat_handler import ChatHandler
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class Operations:

    dom = DOM()

    def main(self):
        content = self.extract_content()
        # GenLogger.info(content)

        if len(content.posts) > 0:
            self.posts_main()
        if len(content.conversations) > 0:
            self.conversations_main(content.conversations)
        pass

    def posts_main(self):

        pass

    @staticmethod
    def conversations_main(conversations):
        for conversation in conversations:
            ChatHandler().main(conversation)
        pass

    def extract_content(self):
        content = DOMContent()
        posts = self.extract_post_content()
        conversations = self.dom.extract_conversations()

        content.set_post(posts)
        content.set_conversation(conversations)

        return content

    def extract_post_content(self):
        posts = self.dom.main_posts()
        return posts

    def extract_conversation_content(self):
        conversations = self.dom.main_conversation()
        return conversations
