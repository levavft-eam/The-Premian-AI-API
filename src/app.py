import logging
from flask import Flask, jsonify, request, g, Response  # type: ignore
from werkzeug.middleware.proxy_fix import ProxyFix  # type: ignore

from src.flows import video_categorization, VIDEO_ID, TRANSCRIPT
from src.common.setup_logging import setup_logging


logger = logging.getLogger(__name__)
setup_logging()


app = Flask(__name__)
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


# .../test
@app.route('/test', methods=['GET'])
def run_test():
    return jsonify(video_categorization(VIDEO_ID, transcript=TRANSCRIPT))


# .../fail
@app.route('/fail', methods=['GET'])
def fail():
    raise Exception("Failing on purpose")


# .../categorize?v_id=<v_id>
@app.route('/categorize', methods=['GET'])
def categorize():
    video_id = request.args.get('v_id')
    return jsonify(video_categorization(video_id))


if __name__ == '__main__':
    app.run()
