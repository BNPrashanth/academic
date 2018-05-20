from log.logger import GeneralLogger
from nltk.tokenize import RegexpTokenizer
from nltk import ne_chunk, pos_tag
from chat_utils import Utils
import enchant
import difflib
import nltk

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
        ne = ne_chunk(pos_tag(tokens))
        ne_set = set()
        for tree in ne:
            if type(tree) is nltk.tree.Tree:
                ne_set.add(tree[0][0])
        english_dict = enchant.Dict("en_US")
        for i in range(len(tokens)):
            if not english_dict.check(tokens[i]) and tokens[i] not in ne_set:
                GenLogger.debug(tokens[i] + " is a MISSPELLED word..")
                # Handling mis-spelled words...
                suggestions = english_dict.suggest(tokens[i])
                dictionary = {}
                maximum = 0
                for suggestion in suggestions:
                    tmp = difflib.SequenceMatcher(None, tokens[i], suggestion).ratio()
                    dictionary[tmp] = suggestion
                    if tmp > maximum:
                        maximum = tmp
                GenLogger.debug(dictionary[maximum])
                tokens[i] = dictionary[maximum]
        tokenized_msg = ""
        for token in tokens:
            tokenized_msg = tokenized_msg + " " + token
        return tokenized_msg

    @staticmethod
    def tokenize(message):
        tokenizer = RegexpTokenizer("[\w']+")
        return tokenizer.tokenize(message)
