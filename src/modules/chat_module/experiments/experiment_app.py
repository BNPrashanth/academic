from flask import Flask, jsonify, request
from handlers.request_handler import Operations
from handlers.chat_handler import ChatHandler
from log.logger import GeneralLogger

Logger = GeneralLogger(__name__)
GenLogger = Logger.init_general_logger()


# Creating a Flask Application
experiment_app = Flask(__name__)

op = Operations()
chat_handler = ChatHandler()


# Test Function to launch the application
@experiment_app.route('/', methods=['GET'])
def test():
    GenLogger.info("TEST")
    return jsonify({'data': 'Excellent...'})


# Test Function to test POST Requests
@experiment_app.route('/test2', methods=['POST'])
def test2():
    GenLogger.info(request.json["data"])
    return jsonify({'data': 'POST Excellent...'})


@experiment_app.route('/chatTextFeature', methods=['POST'])
def chat_get_text_feature():
    """
        For ChatModule, extracts text features of a given message
        @:param     ==>> Message
        @:returns   ==>> Text Feature for the given Message
    """
    GenLogger.info("Starting to identify TextFeatures of message..")
    response = chat_handler.identify_conversation_features(request.json["message"])
    return jsonify({'response': response})


@experiment_app.route('/chatGroupMessages', methods=['POST'])
def chat_get_message_groups():
    """
        For ChatModule, extracts text features of a given message
        @:param     ==>> Message
        @:returns   ==>> Text Feature for the given Message
    """
    GenLogger.info("Starting to Group Messages..")
    response = chat_handler.identify_message_groups(request.json["messageslist"])
    GenLogger.info(response)
    return jsonify({'response': "Success.."})


if __name__ == '__main__':
    experiment_app.run()
