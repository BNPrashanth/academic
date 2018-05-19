import requests
from bs4 import BeautifulSoup
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class FeatureIdentifier:

    """
        Returns Text Features for a given Message.
        [Images, Files and Videos are not considered]

        @:param   ==>> A single message
        @:returns ==>> Text Feature for the given message
    """
    def separator(self, message):
        phrases = message.split()
        is_not_text = False
        msg_text = ""
        for phrase in phrases:
            GenLogger.debug(phrase)
            # If phrase is an image
            if "_IMG_" in phrase:
                msg_text = msg_text + phrase[5:]
                continue
            # If phrase is a hyperlink
            if "http://" in phrase or "https://" in phrase:
                metadata = self.get_metadata(phrase)
                GenLogger.debug("MetaData ==>> " + metadata)
                msg_text = msg_text + metadata + " "
                continue

            # If phrase is an emoticon
            emo_dict = self.get_emoticon_dict()
            for k in emo_dict:
                if k.lower() in phrase:
                    GenLogger.debug("Expression ==>> " + k + " ==> " + emo_dict[k])
                    msg_text = msg_text + emo_dict[k] + " "
                    is_not_text = True

            # If phrase is Text
            if not is_not_text:
                msg_text = msg_text + phrase + " "
        GenLogger.info("Message as TEXT ONLY ==>> \n\t" + message + "\n\t" + msg_text)
        return msg_text

    """
        Returns an Emoticon Dictionary based on the emoji_unicode.txt file.

        @:param   ==>> None
        @:returns ==>> Emoticon Dictionary
    """
    @staticmethod
    def get_emoticon_dict():
        path = "../../resources/emoji_unicode.txt"
        emoticon_file = open(path, 'r')
        emoticon_list = emoticon_file.readlines()
        emoticon_dict = dict()
        for el in emoticon_list:
            element = el.split(" - ")
            emoticon_dict[element[0]] = element[1].split("\n")[0]
        return emoticon_dict

    """
        Returns meta-description of a url.

        @:param   ==>> A url
        @:returns ==>> Meta-Description of the given url 
    """
    @staticmethod
    def get_metadata(url):
        req = requests.get(url)
        res = BeautifulSoup(req.text, 'html.parser')
        meta = res.find_all('meta')
        for m in meta:
            if 'name' in m.attrs and m.attrs['name'] == 'description':
                GenLogger.debug("Description ==>> " + m.attrs['content'])
                return m.attrs['content']
        return ""
