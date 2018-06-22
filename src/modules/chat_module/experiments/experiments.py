from message_grouper import MessageGrouper
from relatedness import Similarity
from gensim.models import Word2Vec, KeyedVectors
import spacy

nlp = spacy.load("en_core_web_lg")


class SimilarityExperiment:

    @staticmethod
    def test_w2v():
        vec = nlp("computer")
        print(vec.vector)

    def main(self):
        # From all sentences, pick pairs
        all_sentences = self.get_sentence_pair()
        print("Similarity\t CosineSim\t CosineSynSim\t SpacySim\t Sentences")
        for sentences in all_sentences:
            s1 = self.get_similarity(sentences)
            s2 = self.get_similarity_cosine(sentences)
            s3 = self.get_similarity_cosine_synset(sentences)
            s4 = Similarity.get_message_similarity_spacy(sentences[0], sentences[1])
            print(round(s1, 3), "\t\t", round(s2, 3), "\t\t", round(s3, 3), "\t\t\t", round(s4, 3), "\t\t\t",
                  sentences[0], " <<>> ", sentences[1])

    @staticmethod
    def get_sentence_pair():
        path = "../chat_resources/related_messages_pair"
        file = open(path, 'r', encoding="utf8")
        lines = file.readlines()
        all_sentences = []
        for line in lines:
            sentences = line.replace("\n", "").split(" <<>> ")
            all_sentences.append(sentences)
        return all_sentences

    @staticmethod
    def get_similarity(sentences):
        grouper = MessageGrouper()
        sim = Similarity()
        score = 0
        if len(sentences) == 2:
            synsetA = sim.get_message_vector_full(grouper.get_sem_words(sentences[0]))
            synsetB = sim.get_message_vector_full(grouper.get_sem_words(sentences[1]))
            try:
                score = sim.get_message_similarity(synsetA, synsetB)
                # print(sentences[0] + " <<>> " + sentences[1])
                # print("\tSimilarity Score ==>> ", score)
            except IndexError:
                # print("error")
                pass
        return score

    @staticmethod
    def get_similarity_cosine_synset(sentences):
        grouper = MessageGrouper()
        sim = Similarity()
        score = 0
        if len(sentences) == 2:
            synsetA = sim.get_message_vector_full(grouper.get_sem_words(sentences[0]))
            synsetB = sim.get_message_vector_full(grouper.get_sem_words(sentences[1]))
            try:
                score = sim.get_message_similarity_cosine(synsetA, synsetB)
                # print(sentences[0] + " <<>> " + sentences[1])
                # print("\tSimilarity Score ==>> ", score)
            except IndexError:
                # print("error")
                pass
        return score

    @staticmethod
    def get_similarity_cosine(sentences):
        sim = Similarity()
        score = 0
        if len(sentences) == 2:
            sentA = sentences[0].split()
            sentB = sentences[1].split()
            try:
                score = sim.get_message_similarity_cosine(sentA, sentB)
                # print(sentences[0] + " <<>> " + sentences[1])
                # print("\tSimilarity Score ==>> ", score)
            except IndexError:
                # print("error")
                pass
        return score


class GroupingExperiment:

    def main(self):
        all_sentences = self.get_sentence_pair()
        for sentences in all_sentences:
            groupedList, ungroupedList = self.get_groups(sentences)
            for group in groupedList:
                print("Group:")
                for sent in group:
                    print("\t", sent)
            for ungrouped in ungroupedList:
                print("Not Grouped:")
                for sent in ungrouped:
                    print("\t", sent)

    @staticmethod
    def get_sentence_pair():
        path = "../chat_resources/related_messages_group"
        file = open(path, 'r', encoding="utf8")
        lines = file.readlines()
        all_sentences = []
        for line in lines:
            sentences = line.replace("\n", "").split(" <<>> ")
            all_sentences.append(sentences)
        return all_sentences

    @staticmethod
    def get_groups(sentences):
        grouper = MessageGrouper()
        grouped, ungrouped = grouper.main(sentences)
        return grouped, ungrouped


exp1 = SimilarityExperiment()
exp1.main()
# exp1.test_w2v()

# exp2 = GroupingExperiment()
# exp2.main()
