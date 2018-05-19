from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class IntentionClassifier:
    @staticmethod
    def test():
        GenLogger.info("Inside Intention Classifier")
