#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import commands
import report_service
import sensor_log_reader
import warning_reader

from flask import request
from flask import Flask, jsonify, url_for

app = Flask(__name__)


@app.route("/stats")
def stats():
    return jsonify(sensor_log_reader.load_data())


@app.route("/records")
def records():
    return jsonify(sensor_log_reader.get_records_for_today())


@app.route("/avg")
def average():
    return jsonify(sensor_log_reader.get_averages())


@app.route("/warns")
def today_warns():
    return jsonify(warning_reader.get_warnings_for_today())


@app.route("/warns/now")
def current_warns():
    return jsonify(sensor_log_reader.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    return jsonify(sensor_log_reader.count_warning_today())


@app.route("/warns/date")
def specific_day_warns():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    return jsonify(warning_reader.get_warnings_for(year, month, day))


@app.route("/now")
def now_two():
    return jsonify(sensor_log_reader.get_last_measurement())


@app.route("/system")
def system():
    return jsonify(commands.get_system_info())


@app.route("/report/yesterday")
def last_report():
    return jsonify(report_service.generate_for_yesterday())


@app.route("/")
def welcome():
    return str(["Warm welcome!",
                (request.host_url + str(url_for('now'))),
                (request.host_url + str(url_for('records'))),
                (request.host_url + str(url_for('today_warns'))),
                (request.host_url + str(url_for('specific_day_warns'))),
                (request.host_url + str(url_for('current_warns'))),
                (request.host_url + str(url_for('system'))),
                (request.host_url + str(url_for('stats')))
                ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
