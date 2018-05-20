class Utils:

    @staticmethod
    def get_emoticon_dict():
        """
            Returns an Emoticon Dictionary based on the emoji_unicode.txt file.

            @:param   ==>> None
            @:returns ==>> Emoticon Dictionary
        """
        path = "../../resources/emoji_unicode.txt"
        emoticon_file = open(path, 'r')
        emoticon_list = emoticon_file.readlines()
        emoticon_dict = dict()
        for el in emoticon_list:
            element = el.split(" - ")
            emoticon_dict[element[0]] = element[1].split("\n")[0]
        return emoticon_dict

    @staticmethod
    def get_abbreviations_dict():
        """
            Returns an Emoticon Dictionary based on the emoji_unicode.txt file.

            @:param   ==>> None
            @:returns ==>> Emoticon Dictionary
        """
        path = "../../resources/abbreviations.txt"
        abbreviations_file = open(path, 'r')
        abbreviations_list = abbreviations_file.readlines()
        abbreviations_dict = dict()
        for el in abbreviations_list:
            element = el.split(" <<>> ")
            abbreviations_dict[element[0].lower()] = element[1].split("\n")[0]
        return abbreviations_dict
