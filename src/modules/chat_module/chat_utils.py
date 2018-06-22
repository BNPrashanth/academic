class Utils:

    @staticmethod
    def get_emoticon_dict():
        """
            Returns an Emoticon Dictionary based on the emoji_unicode.txt file.

            :param   ==>> None
            :returns ==>> Emoticon Dictionary
        """
        path = "../../resources/emoticons.txt"
        emoticon_file = open(path, 'r')
        emoticon_list = emoticon_file.readlines()
        emoticon_file.close()
        emoticon_dict = dict()
        for el in emoticon_list:
            element = el.split(" - ")
            emoticon_dict[element[0]] = element[1].split("\n")[0]
        return emoticon_dict

    @staticmethod
    def get_abbreviations_dict():
        """
            Returns an Emoticon Dictionary based on the abbreviations.txt file.

            :param   ==>> None
            :returns ==>> Abbreviations Dictionary
        """
        path = "../../resources/abbreviations.txt"
        abbreviations_file = open(path, 'r')
        abbreviations_list = abbreviations_file.readlines()
        abbreviations_file.close()
        abbreviations_dict = dict()
        for el in abbreviations_list:
            element = el.split(" <<>> ")
            abbreviations_dict[element[0].lower()] = element[1].split("\n")[0]
        return abbreviations_dict

    @staticmethod
    def get_swear_words():
        """
            Returns a set of SWEAR WORDS which are already identified and kept in the swear_words.txt file

            :param   ==>> None
            :returns ==>> Set of Swear Words
        """
        swear_set = set()
        path = "../../resources/swear_words.txt"
        sw_file = open(path, 'r')
        sw_list = sw_file.readlines()
        sw_file.close()
        for el in sw_list:
            element = el.split(" <<>> ")
            swear_set.add(element[0])
        return swear_set
