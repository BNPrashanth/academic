import nltk
from nltk import sent_tokenize
from nltk import RegexpTokenizer, PorterStemmer
from nltk.corpus import movie_reviews

#POSITIVE- having badword
class context:
    badword_sen= [""]*10
    iter =0;
    post_new = open("Text_resources/PostText1.txt", "r").read()    #taking pure text from PostText1.txt
    print(post_new)

    # def Identify_badword_inclusion(self):
    def MainAnalyser(self,text):    #main method calling badwordz_inclusion check and negation having on that
        bad = self.Identify_badword_inclusion(self.post_new)    #send pure text to check inclusion and receiving having sentence array
        # for ii in bad:
        #     if ii:
        #         print(ii)
        status = self.Status_finder_pos(bad)    #send badword having sentence array and
        #print(status)

    def Identify_badword_inclusion(self,post_new1):
        sentence = sent_tokenize(post_new1)
        badword = open("../../../resources/text_resources/BadWords.txt", "r").read()
        # print(sentence)
        tokenizer = RegexpTokenizer("[\w']+")
        # lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        for i in sentence:
            # print(tokenizer.tokenize(i))
            for j in tokenizer.tokenize(i):
                # print(j,stemmer.stem(j))
                j = stemmer.stem(j)
                # print(j)#lemmas from post text

        #search on bad word dictionary

                for x in badword.split(','):
                    if x == j:  #checking with badword dictionary
                        # print("YES,IT HAS BAD WORD")
                        # print(i)
                        self.badword_sen[self.iter] = i;
                        self.iter+=1;
                        # for xx in self.badword_sen:
                        #     print(xx)
        return self.badword_sen

    #temporaly not called this method
    #search on negative dictionary
    # def Status_finder(self,text3):
    #     count = 0
    #     status_code = 0
    #     status = ""
    #     tokenizer = RegexpTokenizer("[\w']+")
    #     stemmer = PorterStemmer()
    #     for iii in text3:
    #         if iii:
    #             print(iii,end= "")
    #         negative = open("Negations.txt", "r").read()
    #         for iiii in tokenizer.tokenize(iii):
    #             iiii = stemmer.stem(iiii)
    #             for x in negative.split(','):
    #                 if x == iiii:   #checking with negation dictionary
    #                     # print(x,end= "")
    #                     status_code = 1
    #                     count=count+1
    #     #badword having sentence having negation --->POSITIVE SENTENCE
    #         if status_code == 1 and count%2==1 and iii:
    #             status = "POSITIVE"
    #             print(status)
    #         else:
    #             if iii:
    #                 status = "NEGATIVE"
    #                 print("\n",status)
    #     return status

    def Status_finder_pos(self,text3):
        train_text = movie_reviews.words()
        tokenizer = RegexpTokenizer("[\w']+")
        print("It has bad words, should send to classifier")
        for iii in text3:
            if iii:
                print(tokenizer.tokenize(iii))
                tokenized = tokenizer.tokenize(iii)

                try:
                    for i in tokenized:
                        words = nltk.word_tokenize(i)
                        tagged = nltk.pos_tag(words)
                        # print(tagged)
                except Exception as e:
                    print(str(e))

        # for iii in text3:
        #     if iii:
        #         print(tokenizer.tokenize(iii))


contextAnalyse = context()
contextAnalyse.MainAnalyser("From Outside program")
