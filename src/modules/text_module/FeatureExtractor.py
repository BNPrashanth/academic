from log.logger import GeneralLogger
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
from nltk import sent_tokenize

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class FeatureEx:
    post_new = open("../../resources/Post_Trans.txt", "r").read()
    soup = BeautifulSoup(post_new, "html.parser")
    content = soup.get_text()

    feeling = content.split("·")[0]
    comment = ""
    post_content = ""
    for n in soup.find_all('div'):
        if str(n.get('class')) == "['_5pbx', 'userContent', '_3576']":
            content = str(feeling) + str(n.text)
            post_content = content
        if str(n.get('class')) == "['_3b-9', '_j6a']":
            sp_tag = BeautifulSoup(str(n), 'html.parser').find_all('span', class_="UFICommentBody")
            for s in sp_tag:
                comment = comment + ", " + s.text

    content = content + comment
    print("INPUT :", content)
    print("  FEELING :", feeling)
    print("  POST CONTENT :", post_content)

    def Mainfunc(self, text):
        #print("Main func",text)
        filtered_text = self.content

        # hashtag is available in content
        for word in self.content.split():
            if (word.startswith('#')):
                #print(word)
                r = self.Hashtag_handler("*from inside function")
                filtered_text = r
                #print(r)
                break

        #emoticon is available in content
        if self.soup.find_all('img') != []:
            emo = self.Emoticon_handler(filtered_text)
            filtered_text = emo
            #print(emo)

        # url is available in content
        for word in filtered_text.split():
            if (word.startswith('http')):
                url = self.Url_handler(filtered_text)
                filtered_text = url
                #print(url)
                break;

        print("  COMMENTS & REPLIES :", self.comment[1:])
        print("OUTPUT: " + filtered_text)
        return filtered_text


    def Hashtag_handler(self, text2):
        #print("Subfuc", text2)

        hash = ""
        hash_removed = ""
        list = self.content.split()
        for word in self.content.split():
            if (word.startswith('#')):
                hash = word
                word = word[1:]
                # print(word)
            hash_removed = hash_removed + " " + word
        # print(hash_removed)
        hashtag_link = "https://www.facebook.com" + self.soup.a['href'] + "&pnref=story"
        text = self.Metadata_handler(hashtag_link)
        text = self.content.replace(hash, text)
        print("    HASHTAG :", hash[:-2])
        #print(text)
        return text


    def Url_handler(self, text):
        url_removed = ""
        for word in text.split():
            if (word.startswith('http')):
                url_reg = r'[a-z]*[:.]+\S+'
                url_removed = re.search("(?P<url>https?://[^\s]+)", text).group("url")
        text_with_emo = self.Metadata_handler(url_removed)
        text = text.replace(url_removed, text_with_emo)
        print("    URL :", url_removed)
        #print("Output:", text)
        return text

    def Emoticon_handler(self,text):
        emoti = ""
        emoti_src = ""
        for m in (self.soup.find_all('img')):
            src_emo = ((m.get('src'))[-9:])[:5]
            emo_meaning = ""
            # print(src_emo)
            emoticon = open("../../resources/Emoticons_dictionary.txt", "r").read()
            # print(emoticon)
            # print(emoticon.split('\n'))
            for c in emoticon.split('\n'):
                if c.split(':')[0] == src_emo:
                    # print(c.split(':')[1])
                    emo_meaning = c.split(':')[1]
                    emoti_src = c.split(':')[0]

            for n in self.soup.find_all('span'):
                # if n.get('class') == "['_7oe']":
                if str(n.get('class')) == "['_7oe']":
                    # print(n.string)
                    text = text.replace(n.string, " " + emo_meaning)
                    #print("Output:", text)
                    emoti = n.string
        print("    EMOTICON :", emoti, "with src no ",emoti_src)
        return text

    def Metadata_handler(self, link):

        r = requests.get(link)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        meta = soup.find_all('meta')
        # print(meta)
        for m in meta:
            if 'name' in m.attrs and m.attrs['name'] == 'description':
                GenLogger.info("Description ==>> " + m.attrs['content'])
                meta_des = m.attrs['content']
                #print("MetaData: ", meta_des)
        return meta_des[:-1];


extractor = FeatureEx()
extractor.Mainfunc("*from outside function")
