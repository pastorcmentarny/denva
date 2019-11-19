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
import sys
import logging

import averages
import commands
import config_serivce
import email_sender_service
import information_service
import records
import report_service
import sensor_log_reader
import sensor_warnings
import tubes_train_service
import web_data

from flask import Flask, jsonify, url_for,send_file, request, render_template

app = Flask(__name__)
logger = logging.getLogger('stats')


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


@app.route("/log/app")
def recent_log_app():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 300))


@app.route("/log/hc")
def recent_log_hc():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 300))


@app.route("/report/yesterday")
def last_report():
    return jsonify(report_service.generate_for_yesterday())


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data.get_status()
    }
    return jsonify(tt_statuses)


@app.route("/tt/delays")
def tt_delays_counter():
    return jsonify(tubes_train_service.count_tube_problems_today())


@app.route("/tt/counter")
def tt_counter():
    return jsonify(tubes_train_service.count_tube_color_today())


@app.route("/webcam")
def do_picture():
    filename = commands.capture_picture()
    return send_file(filename, mimetype='image/jpeg')


@app.route("/hc")
def healthcheck():
    return jsonify({"status": "UP"})


@app.route("/ricky")
def ricky():
    return jsonify(information_service.get_data_about_rickmansworth())


@app.route('/set/hc')
def set_ip_for_healthcheck():
    host = request.host_url[:-1]
    hc_page = host + str(url_for('healthcheck'))
    config_serivce.update_healthcheck(hc_page)


@app.route("/")
def welcome():
    host = request.host_url[:-1]
    page_now = host + str(url_for('now'))
    print(page_now)
    page_system = host + str(url_for('system'))
    page_avg = host + str(url_for('average'))
    page_records = host + str(url_for('record'))
    page_stats = host + str(url_for('stats'))
    page_warns = host + str(url_for('today_warns'))
    page_warns_now = host + str(url_for('current_warns'))
    page_warns_count = host + str(url_for('count_warns'))
    page_last_report = host + str(url_for('last_report'))
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_tube_trains_counter = host + str(url_for('tt_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_recent_log_hc = host + str(url_for('recent_log_hc'))
    page_webcam = host + str(url_for('do_picture'))
    data = {
        'page_now' : page_now,
        'page_system' : page_system,
        'page_avg' : page_avg,
        'page_records' : page_records,
        'page_stats' : page_stats,
        'page_warns' : page_warns,
        'page_warns_now' : page_warns_now,
        'page_warns_count' : page_warns_count,
        'page_last_report' : page_last_report,
        'page_tube_trains' : page_tube_trains,
        'page_tt_delays_counter' : page_tt_delays_counter,
        'page_tube_trains_counter' : page_tube_trains_counter,
        'page_recent_log_app' : page_recent_log_app,
        'page_recent_log_hc' : page_recent_log_hc,
        'page_webcam' : page_webcam
    }

    return render_template('dashboard.html', message=data)


if __name__ == '__main__':
    logger.info('Starting web server')

    try:
        app.run(debug=True)
        #app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
        healthcheck()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email('web application',
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(e))
        sys.exit(0)
