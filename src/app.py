import logging
from flask import Flask, jsonify, request, g, Response  # type: ignore
from flask_cors import CORS # type: ignore

from werkzeug.middleware.proxy_fix import ProxyFix  # type: ignore
from werkzeug.exceptions import BadRequest # type: ignore

from src.flows import (video_categorization, VIDEO_ID, TRANSCRIPT, youtube_channel_statistics, text_categorization,
                       video_basic_information)
from src.common.setup_logging import setup_logging


logger = logging.getLogger(__name__)
setup_logging()


app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=0, x_host=0, x_prefix=0
    # app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


@app.before_request
def gather_request_data():
    g.method = request.method
    g.url = request.url


@app.after_request
def log_details(response: Response):
    g.status = response.status

    logger.info(f'method: {g.method}\n url: {g.url}\n status: {g.status}')

    return response


def handle_exception(e):
    assert isinstance(e, KeyError)
    logger.error(e, exc_info=True)
    # raise e
    return jsonify({
        "result": False,
        "error message": e.__repr__()
    })


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return handle_exception(e), 400


@app.errorhandler(Exception)
def handle_generic_exception(e):
    return handle_exception(e), 500


@app.route('/test/partial_video_categorization', methods=['GET'])
def run_test():
    return jsonify(video_categorization(VIDEO_ID, transcript=TRANSCRIPT))


@app.route('/test/crash', methods=['GET'])
def fail():
    raise Exception("Crashing on purpose")


# .../categorize?v_id=<v_id>
@app.route('/video/categorize', methods=['GET'])
def categorize():
    url_format = "/video/categorize?v_id=<video id>"
    video_id = request.args.get('v_id')
    if video_id is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    use_openapi_transcription = request.args.get('use_openai', default=False)
    if ((isinstance(use_openapi_transcription, str) and use_openapi_transcription.lower().startswith('t')) or
            (isinstance(use_openapi_transcription, int) and use_openapi_transcription > 0)):
        use_openapi_transcription = True

    return jsonify(video_categorization(video_id, use_openai=use_openapi_transcription))


@app.route('/video/basic_information', methods=['GET'])
def get_basic_information():
    url_format = "/video/basic_information?v_id=<video id>"
    video_id = request.args.get('v_id')
    if video_id is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    return jsonify(video_basic_information(video_id))


@app.route('/text/categorize', methods=['GET'])
def text_categorize():
    url_format = "/text/categorize?text=<text>"
    text = request.args.get('text')
    if text is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")
    
    return jsonify(text_categorization(text))



# .../youtube/channel_statistics?channel_handle=<channel_handle>
@app.route('/youtube/channel_statistics', methods=['GET'])
def channel_statistics():
    channel_handle = request.args.get('channel_handle')
    url_format = "/youtube/channel_statistics?channel_handle=<channel handle>"
    if channel_handle is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    return jsonify(youtube_channel_statistics(channel_handle))


if __name__ == '__main__':
    app.run()
