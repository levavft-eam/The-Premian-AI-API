import logging
from flask import Flask, jsonify, request, g, Response  # type: ignore
from flask_cors import CORS # type: ignore

from werkzeug.middleware.proxy_fix import ProxyFix  # type: ignore
from werkzeug.exceptions import BadRequest  # type: ignore

from src.flows import (video_categorization, VIDEO_ID, TRANSCRIPT, youtube_channel_statistics, text_categorization,
                       video_basic_information, youtube_channel_details)
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


def parse_bool(var, default=False):
    if isinstance(var, bool):
        return var
    if isinstance(var, str):
        if var.lower().startswith('t'):
            return True
        if var.lower().startswith('f'):
            return False
        try:
            var = int(var)
        except:
            raise Exception(f"Couldn't parse {var=} as bool")
    if isinstance(var, int):
        return var > 0
    return default
   

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
    assert isinstance(e, Exception)
    logger.error(e, exc_info=True)

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


@app.route('/video/categorize', methods=['GET'])
def categorize():
    url_format = "/video/categorize?v_id=<video id>"
    truncate = parse_bool(request.args.get("truncate", False))
    use_openapi_transcription = parse_bool(request.args.get('use_openai', default=False))
    video_id = request.args.get('v_id')
    if video_id is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    return jsonify(video_categorization(video_id, use_openai=use_openapi_transcription, truncate=truncate))


@app.route('/video/basic_information', methods=['GET'])
def get_basic_information():
    url_format = "/video/basic_information?v_id=<video id>"
    video_id = request.args.get('v_id')
    if video_id is None:
        raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    return jsonify(video_basic_information(video_id))


@app.route('/text/categorize', methods=['GET', 'POST'])
def text_categorize():
    text = None
    if request.method == "GET":
        url_format = "/text/categorize?text=<text>"
        text = request.args.get('text')
        truncate=request.args.get('truncate', False)
        if text is None:
            raise BadRequest(f"{request.url}. Expected url format: {url_format}")

    elif request.method == "POST":
        text = request.json.get("text")
        truncate = request.json.get("truncate", False)
        if text is None:
            raise BadRequest(f"{request.url}. Expected a json body with a 'text' field. Recieved: {request.json}")

    if text is None:
            raise BadRequest(f"{request.url}.")
    
    return jsonify(text_categorization(text, truncate=truncate))


@app.route('/youtube/channel_statistics', methods=['GET'])
def channel_statistics():
    channel_handle = request.args.get('channel_handle')
    channel_id = request.args.get('channel_id')
    if (channel_handle is channel_id is None) or None not in {channel_id, channel_handle}:
        raise BadRequest(f"{request.url}. Expected exactly one of 'channel_id' and 'channel_handle' to be specified.")

    return jsonify(youtube_channel_statistics(channel_handle, channel_id))


@app.route("/youtube/channel_details", methods=["GET"])
def channel_details():
    channel_handle = request.args.get('channel_handle')
    channel_id = request.args.get('channel_id')
    n = request.args.get('n', 5)

    if (channel_handle is channel_id is None) or None not in {channel_id, channel_handle}:
        raise BadRequest(f"{request.url}. Expected exactly one of 'channel_id' and 'channel_handle' to be specified.")

    return jsonify(youtube_channel_details(channel_handle, channel_id, n))

if __name__ == '__main__':
    app.run()
