import logging


class GeneralLogger:
    isLogInitialized = False

    def __init__(self, class_name):
        self.GenLogger = logging.getLogger(class_name)

    # Initialization of GeneralLogger
    def init_general_logger(self):
        self.GenLogger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:GeneralLogger:%(name)s:%(lineno)d:%(message)s')

        file_handler = logging.FileHandler('../../resources/general_logger.log')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.GenLogger.addHandler(file_handler)
        self.GenLogger.addHandler(stream_handler)

        return self.GenLogger
