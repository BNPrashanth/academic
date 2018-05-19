from bs4 import BeautifulSoup
from util_classes import Post


class Test:

    @staticmethod
    def dom_extractor():
        path = "../../resources/ChatTabsPagelet6.txt"
        dom_file = open(path, 'r', encoding="utf8")
        divs = BeautifulSoup(dom_file, 'html.parser').find_all('div')
        post_cont = []
        for div in divs:
            if 'id' in div.attrs and div.attrs['id'] == 'globalContainer':
                post_cont = BeautifulSoup(str(div), 'html.parser').find_all('div', class_="_4-u2 mbm _4mrt _5v3q _4-u8")
                break

        postList = []
        for postel in post_cont:
            post = Post()
            # print(postel)
            div_contWrapper = BeautifulSoup(str(postel), 'html.parser').find('div', class_="_5pcr userContentWrapper")
            div_post = BeautifulSoup(str(div_contWrapper), 'html.parser').find('div', class_="_1dwg _1w_m _q7o")
            div_title = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="d_jzeu0c5xw z_jzeu0fdqr clearfix")
            div_text = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="_5pbx userContent _3576")
            div_images = BeautifulSoup(str(div_post), 'html.parser').find('div', class_="_3x-2")

            # print(postel.attrs['id'])
            # print(div_title.text.replace("\n", "").replace("  ", ""))
            # print(div_text.text)
            id = postel.attrs['id']
            title = div_title.text.replace("\n", "").replace("  ", "")
            try:
                text = div_text.text.strip()
            except AttributeError:
                text = ""
            images = BeautifulSoup(str(div_images), 'html.parser').find_all('img')
            imagesList = []
            for image in images:
                if 'src' in image.attrs:
                    imagesList.append(image.attrs['src'])
                    # print(image.attrs['ajaxify'])
            post.set_post(id, title, imagesList, text)
            post.display()

        # for post in postList:
        #     print(post)
        pass


t = Test()
t.dom_extractor()
