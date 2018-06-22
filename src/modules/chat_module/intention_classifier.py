from chat_utils import Utils
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()

utils = Utils()


class IntentionClassifier:

    def main(self, message_lists):
        for message_list in message_lists:
            contains_sw = self.identify_sw(message_list)
            if contains_sw:
                return 0
            else:
                return self.predict_chat(message_list)

    @staticmethod
    def identify_sw(messages_list):
        sw_set = utils.get_swear_words()
        for message in messages_list:
            msg = message.split()
            for m in msg:
                if m in sw_set:
                    return True
        return False

    def predict_chat(self, message_list):

        pass

    @staticmethod
    def process_inputs():
        pass
