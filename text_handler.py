class TextHandler:

    def main(self, post_title, post_text): #   GET POST_TEXT AND POST_COMMENT

        pass
pure_txt,output_of_comparison,output_of_classifier,output_of_relativity
    @staticmethod
    def identify_text_features(text):
        """
            Returns text features for each message.
            [Images, Files and Videos are not handled]

            :param   ==>> A single message
            :returns ==>> Text Features of the given message
        """
        pure_txt = FeatureExtractor.FeatureExtract(text)
        return pure_txt

    @staticmethod
    def do_comparison(pure_txt):
        """
            Returns text features for each message.
            [Images, Files and Videos are not handled]

            :param   ==>> A single message
            :returns ==>> Text Features of the given message
        """
        pure_txt = CompareWithDictionary.MainAnalyser(pure_txt)
        return output_of_comparison

    @staticmethod
    def do_classifier(output_of_comparison):
        """
            Returns text features for each message.
            [Images, Files and Videos are not handled]

            :param   ==>> A single message
            :returns ==>> Text Features of the given message
        """
        if output_of_comparison == 'To_Classication':
            output_of_classifier = Classifier.Classification(pure_txt)
        return output_of_classifier

    @staticmethod
    def check_relativity(output):
        """
            Returns text features for each message.
            [Images, Files and Videos are not handled]

            :param   ==>> A single message
            :returns ==>> Text Features of the given message
        """
        if output_of_comparison == False or output_of_classifier == False:
            output_of_relativity = SpamDetectionOnComment.Classification(post_comment)
        return output_of_relativity

    def disbling():
        if output_of_comparison == True or output_of_classifier == True:
            return True #diable the post
        elif output_of_relativity == False:
                return True #diable the comment
        return False

