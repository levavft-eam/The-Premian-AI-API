import logging
from flask import Flask, request  # type: ignore

from src.common.setup_logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging()


app = Flask(__name__)


@app.route('/text/categorize', methods=['GET'])
def text_categorize():
    logger.warn(request.method)
    
    return "hi", 200

@app.route('/text/categorize_long', methods=['POST'])
def text_categorize_long():
    logger.warn(request.method)

    return "hi", 200

@app.route('/text/categorize_both', methods=['GET', 'POST'])
def blahblah():
    logger.warn(request.method)

    return "hi", 200


# @app.route('/text/categorize_long', methods=['POST'])
# def text_categorize_long():
#     logger.warn(request.method)
#     text = request.json.text

#     if text is None:
#             raise BadRequest(f"{request.url}.")
    
#     return jsonify(text_categorization(text))
