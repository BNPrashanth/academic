from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


class IntentionClassifier:
    @staticmethod
    def test():
        GenLogger.info("Inside Intention Classifier")

    def predict_chat(self):
        pass

    def train_classifier(self):
        pass

    def process_inputs(self):
        pass
