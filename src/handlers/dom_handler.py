from bs4 import BeautifulSoup
from utilities.util_classes import Conversation, Message, Post
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class DOM:

    @staticmethod
    def main():
        path = "../../resources/ChatTabsPagelet4.txt"
        dom_file = open(path, 'r', encoding="utf8")
        divs = BeautifulSoup(dom_file, 'html.parser').find_all('div')

        return divs

    def main_posts(self):
        divs = self.main()
        post_cont = []
        for div in divs:
            if 'id' in div.attrs and div.attrs['id'] == 'globalContainer':
                post_cont = BeautifulSoup(str(div), 'html.parser').find_all('div', class_="_4-u2 mbm _4mrt _5v3q _4-u8")
                GenLogger.info("No. of Posts ==>>" + str(len(post_cont)))
                break
        return post_cont

    def main_conversation(self):
        divs = self.main()
        chat_tabs_pagelet_divs = []
        for div in divs:
            if 'id' in div.attrs and div.attrs['id'] == 'ChatTabsPagelet':
                chat_tabs_pagelet_divs = BeautifulSoup(str(div), 'html.parser').find_all('div', class_="_5qi9 _5qib")
                GenLogger.info("No. of Conversations ==>> " + str(len(chat_tabs_pagelet_divs)))
                break
        return chat_tabs_pagelet_divs

    def extract_posts(self):
        post_cont = self.main_posts()
        if len(post_cont) > 0:
            post_list = []
            for postel in post_cont:
                post = Post()
                div_contWrapper = BeautifulSoup(str(postel), 'html.parser').find('div', class_="_5pcr userContentWrapper")
                div_post = BeautifulSoup(str(div_contWrapper), 'html.parser').find('div', class_="_1dwg _1w_m _q7o")
                div_title = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="d_jzeu0c5xw z_jzeu0fdqr clearfix")
                div_text = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="_5pbx userContent _3576")
                div_images = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="_3x-2")

                # print(postel.attrs['id'])
                # print(div_title.text.replace("\n", "").replace("  ", ""))
                # print(div_text.text)
                iden = postel.attrs['id']
                title = div_title.text.replace("\n", "").replace("  ", "")
                try:
                    text = div_text.text.strip()
                except AttributeError:
                    text = ""
                images = BeautifulSoup(str(div_images), 'html.parser').find_all('img')
                imagesList = []
                for image in images:
                    if 'src' in image.attrs:
                        imagesList.append(image.attrs['src'])
                        # print(image.attrs['ajaxify'])
                post.set_post(iden, title, imagesList, text)
                post.display()
                post_list.append(post)
            return post_list
        return []

    def extract_conversations(self):
        chat_tabs_pagelet_divs = self.main_conversation()
        if len(chat_tabs_pagelet_divs) > 0:
            conversations_list = []
            for conversation_div in chat_tabs_pagelet_divs:
                title_div = BeautifulSoup(str(conversation_div), 'html.parser').find_all('div', class_="clearfix fbNubFlyoutTitlebar titlebar")
                title_txt = BeautifulSoup(str(title_div[0]), 'html.parser').find_all('a', class_="titlebarText")
                conv_title = title_txt[0].text

                conv_div = BeautifulSoup(str(conversation_div), 'html.parser').find_all('div', class_="_1ia _2sz2")
                sender_msgs_global = BeautifulSoup(str(conv_div), 'html.parser').find_all('div', class_="_4tdt _ua1")

                messages = []
                for global_msg_div in sender_msgs_global:
                    sender_msgs_local = BeautifulSoup(str(global_msg_div), 'html.parser').find_all('div', class_="_h8t")
                    time_tag = BeautifulSoup(str(global_msg_div), 'html.parser').find_all('a', class_="_4tdw")
                    time = time_tag[0].attrs['aria-label'][len(conv_title) + 1:]

                    for msg in sender_msgs_local:
                        message = Message()
                        msg_a = BeautifulSoup(str(msg), 'html.parser').find_all('span', class_="_5yl5")
                        if msg_a:
                            if msg_a[0].img:
                                msg_comp = msg_a[0].text.replace("\n", "")
                                msg_comp = msg_comp + " " + self.get_emoticon_unicode(msg_a)
                                if "http://" in msg_a[0].text or "https://" in msg_a[0].text:
                                    message.set_message(time, msg_comp, "3")
                                else:
                                    message.set_message(time, msg_comp, "1")
                                # message.display()
                                messages.append(message)
                            else:
                                if "http://" in msg_a[0].text or "https://" in msg_a[0].text:
                                    message.set_message(time, msg_a[0].text.replace("\n", ""), "3")
                                else:
                                    message.set_message(time, msg_a[0].text.replace("\n", ""), "0")
                                # message.display()
                                messages.append(message)
                        else:
                            msg_b = BeautifulSoup(str(msg), 'html.parser').find_all('div', class_="_4yp9")
                            if msg_b:
                                for m in msg_b:
                                    if 'style' in m.attrs:
                                        msg_b = "_IMG_" + m.attrs['style'].split("\"")[1]
                                        message.set_message(time, msg_b, "2")
                                        # message.display()
                                        messages.append(message)
                            else:
                                msg_c = BeautifulSoup(str(msg), 'html.parser').find_all('div', class_="")
                                for m in msg_c:
                                    if 'aria-label' in m.attrs:
                                        msg_c = m.attrs['aria-label']
                                        message.set_message(time, msg_c, "4")
                                        # message.display()
                                        messages.append(message)
                con = Conversation()
                con.set_conversation(conv_title, messages)
                conversations_list.append(con)
                con.display()
            # GenLogger.info("Final List ==>> ")
            return conversations_list
        return []

    @staticmethod
    def get_emoticon_unicode(msg_a):
        msg_comp = ""
        for img in BeautifulSoup(str(msg_a), 'html.parser').find_all('img'):
            if img.attrs['src']:
                img_url_list = img.attrs['src'].split("/")
                img_unicode = img_url_list[len(img_url_list) - 1]
                img_unicode = img_unicode[0:5]
                msg_comp = msg_comp + " " + img_unicode
        return msg_comp
