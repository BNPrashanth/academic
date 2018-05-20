from log.logger import GeneralLogger
from nltk.tokenize import RegexpTokenizer
from chat_utils import Utils
import enchant

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()

utils = Utils()


class PreProcessor:

    def main_pre_process(self, message):
        abbreviations_dict = utils.get_abbreviations_dict()
        word_list = message.split()
        new_message = ""
        for word in word_list:
            if word.lower() in abbreviations_dict:
                expansion = abbreviations_dict[word.lower()]
                new_message = new_message + " " + expansion
            else:
                new_message = new_message + " " + word
        tokens = self.tokenize(new_message)
        english_dict = enchant.Dict("en_US")
        for i in range(len(tokens)):
            if not english_dict.check(tokens[i]):
                GenLogger.debug(tokens[i] + " is a MISSPELLED word..")
                # Handling mis-spelled words...
                # tokens[i] = tokens[i] + "_MISSPELLED_WORD"
        tokenized_msg = ""
        for token in tokens:
            tokenized_msg = tokenized_msg + " " + token
        return tokenized_msg

    @staticmethod
    def tokenize(message):
        tokenizer = RegexpTokenizer("[\w']+")
        return tokenizer.tokenize(message)
