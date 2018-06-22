from nltk.corpus import wordnet as wn, stopwords
from nltk import word_tokenize, pos_tag
from relatedness import Similarity
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()

stop_words = set(stopwords.words("english"))


class MessageGrouper:

    sim = Similarity()
    sim_measure = wn.path_similarity
    expected_score = 0.4

    def main(self, messageList):
        messageSynsetList = []
        groupedMsgList = []
        groupedCompleteMsgList = []
        for message in messageList:
            try:
                semWords = self.get_sem_words(message.content)
                synsetList = self.sim.get_message_vector_full(semWords, self.sim_measure)
                GenLogger.info("Synsets for: " + message.content)
                GenLogger.info(synsetList)
            except AttributeError:
                semWords = self.get_sem_words(message)
                synsetList = self.sim.get_message_vector_full(semWords, self.sim_measure)
                GenLogger.info("Synsets for: " + message)
                GenLogger.info(synsetList)
            if len(synsetList) > 0:
                messageSynsetList.append(synsetList)
        GenLogger.debug(messageSynsetList)
        for msgSynset in messageSynsetList:
            for wordSynset in msgSynset:
                try:
                    GenLogger.debug(str(wordSynset) + " ==>> " + wordSynset._definition)
                except AttributeError:
                    GenLogger.error(str(wordSynset) + "has no attribute definition..")
        grouped, ungrouped, indexes, ungp_indexes = self.sim.get_message_group(messageSynsetList, self.expected_score)
        groupedMsgList.append(grouped)
        completeMsgGroup = []
        for i in indexes:
            completeMsgGroup.append(messageList[i])
        groupedCompleteMsgList.append(completeMsgGroup)
        completeMsgUngp = []
        for j in ungp_indexes:
            completeMsgUngp.append(messageList[j])
        if len(ungrouped) > 1:
            while True:
                ungpMsgList = completeMsgUngp
                lenUngp = len(ungrouped)
                gp, ungp, ind, ungpind = self.sim.get_message_group(ungrouped, self.expected_score)
                if lenUngp == len(ungp):
                    break
                ungrouped = ungp
                groupedMsgList.append(gp)
                completeMsgGroup = []
                for i in ind:
                    completeMsgGroup.append(ungpMsgList[i])
                groupedCompleteMsgList.append(completeMsgGroup)
                completeMsgUngp = []
                for j in ungpind:
                    completeMsgUngp.append(ungpMsgList[j])
        for mList in groupedMsgList:
            GenLogger.debug("Group List..")
            for m in mList:
                GenLogger.debug(m)
        print(groupedCompleteMsgList)
        return groupedCompleteMsgList, groupedMsgList

    @staticmethod
    def get_sem_words(sent):
        tags = pos_tag(word_tokenize(sent), tagset="universal")
        GenLogger.debug(tags)
        GenLogger.debug(stop_words)
        semWords = []
        for el in tags:
            if (el[1].lower() == "verb" or el[1].lower() == "noun" or el[1].lower() == "adj") \
                    and el[0].lower() not in stop_words:
                semWords.append(el)
        GenLogger.debug(semWords)
        return semWords

    def get_similarity_hard(self, semWords):
        pass
