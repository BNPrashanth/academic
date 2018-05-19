from log.logger import GeneralLogger
from nltk.tokenize import RegexpTokenizer
import enchant

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class PreProcessor:
    @staticmethod
    def test():
        GenLogger.info("Inside PreProcessor")

    def main_pre_process(self, message):
        tokens = self.tokenize(message)
        english_dict = enchant.Dict("en_US")
        for i in range(len(tokens)):
            if not english_dict.check(tokens[i]):
                GenLogger.debug(tokens[i] + " is a MISSPELLED word..")
                tokens[i] = tokens[i] + "_MISSPELLED_WORD"
        return tokens

    @staticmethod
    def tokenize(message):
        tokenizer = RegexpTokenizer("[\w']+")
        return tokenizer.tokenize(message)
