import spacy
import PyPDF2


path = "/home/bnprashanth/MyFiles/134215A/Project/AK/knowledge_management_book.pdf"

pdf_file = open(path, 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)

chapter_cur = 11
chapter_end = 18
replace_text = ["CHAPTER 1 Concept of Knowledge", "Chapter 1 - Concept of Knowledge"]
page = ""
i = 1
while chapter_end >= chapter_cur:
    cur_page = read_pdf.getPage(chapter_cur).extractText()
    for text in replace_text:
        cur_page = cur_page.replace(text, "")
    cur_page = cur_page.replace("\n" + str(i), "").replace("\n", "")
    page = page + cur_page
    i += 1
    chapter_cur += 1

# print(page)
#
nlp = spacy.load('en_core_web_sm')
docs = nlp(str(page))
for chunk in docs.noun_chunks:
    print(chunk.text)
