import logging


class GeneralLogger:

    def __init__(self, class_name):
        self.GenLogger = logging.getLogger(class_name)
        self.ExpLogger = logging.getLogger(class_name)

    # Initialization of GeneralLogger
    def init_general_logger(self):
        self.GenLogger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:GeneralLogger:%(name)s:%(lineno)d:%(message)s')

        file_handler = logging.FileHandler('/home/bnprashanth/PycharmProjects/FaceBookCompanion/resources/general_logger.log')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.GenLogger.addHandler(file_handler)
        self.GenLogger.addHandler(stream_handler)

        return self.GenLogger

    # Initialization of GeneralLogger
    def init_experiment_logger(self):
        self.ExpLogger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:GeneralLogger:%(name)s:%(lineno)d:%(message)s')

        file_handler = logging.FileHandler('../../resources/experiment_logger.log')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.ExpLogger.addHandler(file_handler)
        self.ExpLogger.addHandler(stream_handler)

        return self.ExpLogger
