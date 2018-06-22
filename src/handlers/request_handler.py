from dom_handler import DOM
from utilities.util_classes import DOMContent
from chat_handler import ChatHandler
from image_handler import ImageHandler
from text_handler import TextHandler
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class Operations:

    dom = DOM()

    def main(self):
        content = self.extract_content()
        # GenLogger.info(content)

        post_res = []
        chat_res = []
        if len(content.posts) > 0:
            post_res = self.posts_main(content.posts)
        if len(content.conversations) > 0:
            chat_res = self.conversations_main(content.conversations)
        return post_res, chat_res

    @staticmethod
    def posts_main(posts_list):
        res_list = []
        for post in posts_list:
            # Send to Text Module
            text_app = TextHandler().main(post.title, post.text)
            # Send to Image Module
            image_app = ImageHandler().main(post.images)
            res_list.append((post.id, text_app, image_app))
        return res_list

    @staticmethod
    def conversations_main(conversations):
        res_list = []
        for conversation in conversations:
            app = ChatHandler().main(conversation)
            res_list.append((conversation.title, app))
        return res_list

    def extract_content(self):
        content = DOMContent()
        posts = self.dom.extract_posts()
        conversations = self.dom.extract_conversations()

        content.set_post(posts)
        content.set_conversation(conversations)

        return content
