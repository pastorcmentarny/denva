import sensor_log_reader
import warning_reader
from flask import request
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


@app.route("/warns")
def today_warns():
    return jsonify(warning_reader.get_warnings_for_today())


@app.route("/warns/data")
def day_warns():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    return jsonify(warning_reader.get_warnings_for(year, month, day))


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
