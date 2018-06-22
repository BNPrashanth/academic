from modules.chat_module.feature_identifier import FeatureIdentifier
from modules.chat_module.preprocessor import PreProcessor
from modules.chat_module.message_grouper import MessageGrouper
from modules.chat_module.intention_classifier import IntentionClassifier
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()

chat_feature_identifier = FeatureIdentifier()
preprocessor = PreProcessor()
classifier = IntentionClassifier()


class ChatHandler:

    def main(self, conversations):
        """
            Returns Intention exhibited by each Chatter in a Conversation

            :param   ==>> List of Conversations
            :returns ==>> Nature of Intention of the Chatter
        """
        for conversation in conversations:
            for msg in conversation.messages:
                if msg.msg_type == 2:
                    msg.content = "image"
                else:
                    msg.content = self.identify_conversation_features(msg.content)
            message_lists, message_synset_lists = self.identify_message_groups(conversation.messages)
            GenLogger.info(message_lists)
            GenLogger.info(message_synset_lists)
            for message_list in message_lists:
                intention_class = self.identify_intention(message_list)
                if intention_class == 0:
                    return 0
        return 1

    @staticmethod
    def identify_conversation_features(messages):
        """
            Returns text features for each message.
            [Images, Files and Videos are not handled]

            :param   ==>> A single message
            :returns ==>> Text Features of the given message
        """
        only_txt = chat_feature_identifier.separator(messages)
        preprocessed_txt = preprocessor.main_pre_process(only_txt)
        return preprocessed_txt

    @staticmethod
    def identify_message_groups(messages):
        """
            Returns lists of grouped messages for a list of messages.

            :param   ==>> A list of messages (only text features)
            :returns ==>> Grouped lists of messages
        """
        message_grouper = MessageGrouper()
        messages_list, message_synset_list = message_grouper.main(messages)
        return messages_list, message_synset_list

    @staticmethod
    def identify_intention(messages_list):
        """
            Returns classified result (class) of grouped messages.

            :param   ==>> A grouped list of messages
            :returns ==>> Intention class (either 0 or 1)
        """
        intention_classifier = IntentionClassifier()
        intention = intention_classifier.main(messages_list)
        return intention
