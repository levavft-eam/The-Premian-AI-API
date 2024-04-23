from flask import Flask, jsonify
from flows import video_categorization, VIDEO_ID, TRANSCRIPT

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


# TODO: use the following links to improve the project if needed
# https://github.com/bajcmartinez/flask-api-starter-kit/tree/master
# https://auth0.com/blog/best-practices-for-flask-api-development/

@app.route('/test', methods=['GET'])
def run_test():
    return jsonify(video_categorization(VIDEO_ID, transcript=TRANSCRIPT))


if __name__ == '__main__':
    app.run()
