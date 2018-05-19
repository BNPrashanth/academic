from nltk.corpus import wordnet as wn, stopwords
from nltk import word_tokenize, pos_tag
from relatedness import Similarity
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class MessageGrouper:

    sim = Similarity()
    sim_measure = wn.path_similarity

    def main(self, messageList):
        messageSynsetList = []
        groupedMsgList = []
        for message in messageList:
            try:
                semWords = self.get_nouns_and_verbs(message.content)
                synsetList = self.sim.get_message_vector_full(semWords, self.sim_measure)
                GenLogger.info("Synsets for: " + message.content)
                GenLogger.info(synsetList)
            except AttributeError:
                semWords = self.get_nouns_and_verbs(message)
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
        grouped, ungrouped = self.sim.get_message_group(messageSynsetList, 0.4)
        groupedMsgList.append(grouped)
        if len(ungrouped) > 1:
            lenUngp = len(ungrouped)
            while True:
                gp, ungp = self.sim.get_message_group(ungrouped, 0.4)
                if lenUngp == len(ungp):
                    break
                groupedMsgList.append(gp)
                lenUngp = len(ungp)
        for mList in groupedMsgList:
            GenLogger.debug("Group List..")
            for m in mList:
                GenLogger.debug(m)
        return groupedMsgList

    @staticmethod
    def get_nouns_and_verbs(sent):
        tags = pos_tag(word_tokenize(sent), tagset="universal")
        GenLogger.debug(tags)
        stop_words = set(stopwords.words("english"))
        GenLogger.debug(stop_words)
        semWords = []
        for el in tags:
            if (el[1].lower() == "verb" or el[1].lower() == "noun") and el[0].lower() not in stop_words:
                semWords.append(el)
        GenLogger.debug(semWords)
        return semWords

    def get_similarity_hard(self, semWords):
        pass
