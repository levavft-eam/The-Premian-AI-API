from flask import Flask, jsonify, request # type: ignore
from src.flows import video_categorization, VIDEO_ID, TRANSCRIPT

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


# TODO: use the following links to improve the project if needed
# https://github.com/bajcmartinez/flask-api-starter-kit/tree/master
# https://auth0.com/blog/best-practices-for-flask-api-development/


# .../test
@app.route('/test', methods=['GET'])
def run_test():
    return jsonify(video_categorization(VIDEO_ID, transcript=TRANSCRIPT))


# .../test
@app.route('/fail', methods=['GET'])
def fail():
    raise Exception("Failing on purpose")

# .../categorize?v_id=<v_id>
@app.route('/categorize', methods=['GET'])
def categorize():
    video_id = request.args.get('v_id')
    return jsonify(video_categorization(video_id, transcript=TRANSCRIPT))  # TODO: remove transcript=TRANSCRIPT


if __name__ == '__main__':
    app.run()
