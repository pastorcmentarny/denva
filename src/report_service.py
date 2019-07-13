import sensor_log_reader
from flask import Flask, jsonify

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
app = Flask(__name__)


@app.route("/stats")
def stats():
    return jsonify(sensor_log_reader.load_data())


@app.route("/records")
def records():
    return jsonify(sensor_log_reader.get_records())


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_current_measurement())


@app.route("/")
def welcome():
    return "Warm welcome!"


def main():
    print("Application started..")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    main()
