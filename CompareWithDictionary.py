from nltk import sent_tokenize
from nltk import RegexpTokenizer,PorterStemmer

#POSITIVE- having badword
class context:
    iter =0;
    post_new = open("PostText1.txt", "r").read()    #taking pure text from PostText1.txt
    print(post_new)
    # def Identify_badword_inclusion(self):
    def MainAnalyser(self,text):    #main method calling badwords_inclusion check and negation having on that
        improper_status = self.Identify_improper_badword_inclusion(self.post_new)    #send pure text to check inclusion and receiving having sentence array
        if improper_status == False:
            bad_status = self.Identify_badword_inclusion(self.post_new)
            if bad_status == True:
                return 'To_Classication'
            else:
                return 'To_SpamDetection'
        else:
            return 'To_Disable'

    def Identify_improper_badword_inclusion(self,post_new1):
        sentence = sent_tokenize(post_new1)
        improper_badword = open("../../../resources/text_resources/ImproperWords.txt", "r").read()
        tokenizer = RegexpTokenizer("[\w']+")
        stemmer = PorterStemmer()
        for i in sentence:
            for j in tokenizer.tokenize(i):
                j = stemmer.stem(j)
                #search on improper bad word dictionary
                for x in improper_badword.split(','):
                    if x == j:  #checking with improper badword dictionary
                        return True
        return False

    def Identify_badword_inclusion(self,post_new1):
        sentence = sent_tokenize(post_new1)
        badword = open("../../../resources/text_resources/BadWords.txt", "r").read()
        tokenizer = RegexpTokenizer("[\w']+")
        stemmer = PorterStemmer()
        for i in sentence:
            for j in tokenizer.tokenize(i):
                j = stemmer.stem(j)
                #search on bad word dictionary
                for x in badword.split(','):
                    if x == j:  #checking with badword dictionary
                        return True
        return False

contextAnalyse = context()
contextAnalyse.MainAnalyser("From Outside program")
