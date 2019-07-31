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
import averages
import records
import sensor_warnings
import report_service
import sensor_log_reader

from flask import request
from flask import Flask, jsonify, url_for

app = Flask(__name__)


@app.route("/stats")
def stats():
    return jsonify(sensor_log_reader.load_data_for_today())


@app.route("/records")
def record():
    return jsonify(records.get_records_for_today())


@app.route("/avg")
def average():
    return jsonify(averages.get_averages_for_today())


@app.route("/warns")
def today_warns():
    return jsonify(sensor_warnings.get_warnings_for_today())


@app.route("/warns/now")
def current_warns():
    return jsonify(sensor_warnings.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    return jsonify(sensor_warnings.count_warning_today())


@app.route("/warns/date")
def specific_day_warns():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    return jsonify(sensor_warnings.get_warnings_for(year, month, day))


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_last_measurement())


@app.route("/system")
def system():
    return jsonify(commands.get_system_info())


@app.route("/report/yesterday")
def last_report():
    return jsonify(report_service.generate_for_yesterday())


@app.route("/")
def welcome():
    host = request.host_url[:-1]
    now = host + str(url_for('now'))
    system = host + str(url_for('system'))
    avg = host + str(url_for('average'))
    records = host + str(url_for('record'))
    stats = host + str(url_for('stats'))
    warns = host + str(url_for('today_warns'))
    warns_now = host + str(url_for('current_warns'))
    warns_count = host + str(url_for('count_warns'))
    last_report = host + str(url_for('last_report'))

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Denva - Dom's Environment Analyser</title>
</head>
<body>
<h1>Select:</h1>
<ul><li><a href="{}">Report for yesterday</a></li></ul>

<h2>Info</h2>   
<ul>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
</ul>
<h2>Warnings:</h2>
<ul>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
    <li><a href="{}">{}</a></li>
</ul>
By Dominik(Pastor Cmentarny)&Omega;(<a href="https://dominiksymonowicz.com/">My homepage</a>)
</body>
</html>""".format(last_report, now, now, records, records, avg, avg, stats, stats, system, system,
                  warns, warns, warns_now, warns_now, warns_count, warns_count)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
