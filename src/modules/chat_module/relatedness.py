from nltk.corpus import wordnet as wn
import numpy as np
import math
import spacy
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()

nlp = spacy.load("en_core_web_lg")


class Similarity:

    @staticmethod
    def get_message_vector_binary(semWords, sim_measure=wn.path_similarity):
        synsetList = []
        for i in range(len(semWords)):
            if i < len(semWords) - 1:
                synsets = wn.synsets(semWords[i][0], pos=semWords[i][1][0].lower())
                # print(synsets)
                max_similarity = 0
                best_pair = {}
                for synset in synsets:
                    # print(synset)
                    nextSynsets = wn.synsets(semWords[i+1][0], pos=semWords[i+1][1][0].lower())
                    for nextSynset in nextSynsets:
                        similarity = sim_measure(synset, nextSynset)
                        print("Similarity between==>> ", synset, " and ", nextSynset, " ==>> ", similarity)
                        if similarity:
                            if similarity > max_similarity:
                                max_similarity = similarity
                                best_pair["w1"] = synset
                                best_pair["w2"] = nextSynset
                try:
                    print(best_pair["w1"], best_pair["w2"])
                    if len(synsetList) == 0:
                        synsetList.append(best_pair["w1"])
                        synsetList.append(best_pair["w2"])
                    elif synsetList[len(synsetList)-1].__eq__(best_pair["w1"]):
                        synsetList.append(best_pair["w2"])
                    else:
                        wordLeft = wn.synsets(synsetList[len(synsetList)-1]._name.split(".")[0])
                        wordRight = wn.synsets(best_pair["w1"]._name.split(".")[0])
                        isSame = False
                        for word_l in wordLeft:
                            for word_r in wordRight:
                                if word_l.__eq__(word_r):
                                    isSame = True
                                    break
                        if isSame:
                            additional_L = 0.0
                            additional_R = 0.0
                            if synsetList[len(synsetList)-2]._name.split(".")[1] == 'v':
                                additional_L = 0.02
                            if best_pair["w1"]._name.split(".")[1] == 'v':
                                additional_R = 0.02
                            leftS1 = sim_measure(synsetList[len(synsetList)-2], synsetList[len(synsetList)-1])
                            leftS2 = sim_measure(synsetList[len(synsetList)-1], best_pair["w2"])
                            rightS1 = sim_measure(synsetList[len(synsetList)-2], best_pair["w1"])
                            rightS2 = sim_measure(best_pair["w1"], best_pair["w2"])

                            try:
                                print("/////////////////", leftS1 + leftS2 + additional_L)
                                print("/////////////////", rightS1 + rightS2 + additional_R)
                                if (leftS1 + leftS2 + additional_L) / 2 > (rightS1 + rightS2 + additional_R) / 2:
                                    synsetList.append(best_pair["w2"])
                                else:
                                    synsetList[len(synsetList) - 1] = (best_pair["w1"])
                                    synsetList.append(best_pair["w2"])
                            except TypeError:
                                print("Exception occured: The 2 words are similar, but no similarity found")
                        else:
                            synsetList.append(best_pair["w1"])
                            synsetList.append(best_pair["w2"])
                except KeyError:
                    print("Exception Handled..")
        # print(synsetList)
        return synsetList

    @staticmethod
    def get_message_vector_full(semWords, sim_measure=wn.path_similarity):
        synsetList = []
        if len(semWords) == 1:
            synsetList.append(wn.synsets(semWords[0][0], pos=semWords[0][1][0].lower())[0])
            return synsetList
        for i in range(len(semWords)):
            synsets = wn.synsets(semWords[i][0], pos=semWords[i][1][0].lower())
            max_similarity = 0.0
            bestSynset = None
            for synset in synsets:
                GenLogger.debug(synset)
                sim = 0.0
                count = 0
                for j in range(len(semWords)):
                    if j != i:
                        otherSynsets = wn.synsets(semWords[j][0], pos=semWords[j][1][0].lower())
                        for other in otherSynsets:
                            if i < j:
                                similarity = sim_measure(synset, other)
                                GenLogger.debug("Similarity between==>> ", synset, " and ", other, " ==>> ", similarity)
                            else:
                                similarity = sim_measure(other, synset)
                                GenLogger.debug("Similarity between==>> ", other, " and ", synset, " ==>> ", similarity)
                            try:
                                sim = sim + similarity
                            except TypeError:
                                sim = sim + 0.0
                            count += 1
                try:
                    res = sim/count
                except ZeroDivisionError:
                    res = 0
                GenLogger.debug("Similarity Score >>>>>>>>>>>>>>> ", res)
                if res > max_similarity:
                    max_similarity = res
                    bestSynset = synset
                elif res == 0:
                    bestSynset = synsets[0]
            GenLogger.debug("BEST >>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", bestSynset)
            if bestSynset:
                synsetList.append(bestSynset)
        return synsetList

    @staticmethod
    def get_message_similarity(sent_vec_A, sent_vec_B, sim_measure=wn.path_similarity):
        GenLogger.debug("\nSentence Similarity..")
        similarity_score = 0
        for synsetA in sent_vec_A:
            for synsetB in sent_vec_B:
                try:
                    similarity_score = similarity_score + sim_measure(synsetA, synsetB)
                    # print("Similarity between==>> ", synsetA, " and ", synsetB, " ==>> ", sim_measure(synsetA, synsetB))
                except TypeError:
                    try:
                        similarity_score = similarity_score + sim_measure(synsetB, synsetA)
                        # print("Similarity between==>> ", synsetA, " and ", synsetB, " ==>> ", sim_measure(synsetB, synsetA))
                    except TypeError:
                        similarity_score = similarity_score + 0.0
        try:
            similarity = 4 * (similarity_score/(len(sent_vec_A) * len(sent_vec_B)))
        except ZeroDivisionError:
            similarity = 0
        GenLogger.debug("Total Similarity Score: " + str(similarity_score))
        GenLogger.debug("Similarity: " + str(similarity))
        return similarity

    def get_message_similarity_cosine(self, sent_vec_A, sent_vec_B):
        GenLogger.debug("\nSentence Similarity - Cosine..")
        # GenLogger.info("Similarity for:" + sent_vec_A + " <<and>> " + sent_vec_B + ":")
        wordsList = []
        for synset in sent_vec_A:
            if synset not in wordsList:
                wordsList.append(synset)
        for synset in sent_vec_B:
            if synset not in wordsList:
                wordsList.append(synset)
        vecA, vecB = [], []
        for word in wordsList:
            count = 0
            for synset in sent_vec_A:
                if word.__eq__(synset):
                    count += 1
            vecA.append(count)
        for word in wordsList:
            count = 0
            for synset in sent_vec_B:
                if word.__eq__(synset):
                    count += 1
            vecB.append(count)
        sim = self.cosine_similarity(np.array(vecA), np.array(vecB))
        return sim

    @staticmethod
    def get_message_similarity_spacy(sentA, sentB):
        vecA = nlp(sentA)
        vecB = nlp(sentB)
        return vecA.similarity(vecB)


    def get_message_group(self, messagesList, score, sim_method=get_message_similarity):
        ungroupedMessages = []
        i = 0
        msgGroup = []
        groupedIndexes = []
        while i < len(messagesList):
            GenLogger.debug("inside 1st..")
            msg = messagesList[i]
            similarity_found = False
            if len(messagesList[i]) < 2:
                # msgGroup.append(messagesList[i])
                i += 1
                continue
            j = i + 1
            while j < len(messagesList):
                GenLogger.debug("Inside 2nd")
                if i < j < len(messagesList):
                    try:
                        if len(messagesList[j]) < 2:
                            # msgGroup.append(messagesList[j])
                            i = j
                            break
                        else:
                            try:
                                if self.get_message_similarity(msg, messagesList[j]) >= score:
                                    print(msg, messagesList[j], " are similar..")
                                    similarity_found = True
                                    if len(msgGroup) != 0 and msgGroup[len(msgGroup) - 1].__eq__(msg):
                                        msgGroup.append(messagesList[j])
                                        groupedIndexes.append(j)
                                    else:
                                        msgGroup.append(msg)
                                        msgGroup.append(messagesList[j])
                                        groupedIndexes.append(i)
                                        groupedIndexes.append(j)
                                    i = j
                                    GenLogger.debug("Breakinggg..")
                                    break
                            except TypeError:
                                GenLogger.error("Similarity not Found..")
                    except IndexError:
                        GenLogger.error("Out of Range..")
                    j += 1
            if not similarity_found:
                i += 1
        for msg in messagesList:
            if msg not in msgGroup:
                ungroupedMessages.append(msg)
        ungroupedIndexes = []
        for i in range(len(messagesList)):
            if messagesList[i] not in msgGroup:
                ungroupedIndexes.append(i)
        return msgGroup, ungroupedMessages, groupedIndexes, ungroupedIndexes

    @staticmethod
    def dot_product(v1, v2):
        return sum(map(lambda x: x[0] * x[1], zip(v1, v2)))

    def cosine_similarity(self, v1, v2):
        prod = self.dot_product(v1, v2)
        len1 = math.sqrt(self.dot_product(v1, v1))
        len2 = math.sqrt(self.dot_product(v2, v2))
        try:
            return prod / (len1 * len2)
        except ZeroDivisionError:
            return 0
        except RuntimeWarning:
            return 0
