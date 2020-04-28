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
import logging

import sys
from flask import Flask, jsonify, url_for, request, render_template

import config_service
from common import data_files, commands
from denva import denva_service, denva_sensors_service
from reports import averages, records
from services import email_sender_service, common_service
from services import sensor_warnings_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Denva UI'


@app.route("/stats")
def stats():
    logger.info('Get all stats for today')
    return jsonify(denva_service.get_all_stats_for_today())


@app.route("/records")
def record():
    logger.info('Getting record measurement from today')
    return jsonify(records.get_records_for_today())


@app.route("/avg")
def average():
    logger.info('Getting average measurement from today')
    return jsonify(averages.get_averages_for_today())


@app.route("/warns")
def today_warns():
    logger.info('Getting all warnings from today')
    return jsonify(sensor_warnings_service.get_warnings_for_today())


@app.route("/warns/now")
def current_warns():
    logger.info('Getting current warnings')
    return jsonify(sensor_warnings_service.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    logger.info('Getting warnings count')
    return jsonify(denva_sensors_service.count_warnings(sensor_warnings_service.get_warnings_for_today()))


@app.route("/warns/date")
def specific_day_warns():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    logger.info('Getting warnings for {}.{}.{}'.format(day, month, year))
    return jsonify(sensor_warnings_service.get_warnings_for(year, month, day))


@app.route("/now")
def now():
    logger.info('Getting last measurement')
    return jsonify(denva_sensors_service.get_last_measurement())


@app.route("/system")
def system():
    logger.info('Getting information about system')
    return jsonify(common_service.get_system_info())


@app.route("/log/system")
def recent_system_log_app():
    logger.info('Getting system logs')
    return jsonify(commands.get_system_logs(200))


@app.route("/log/app")
def log_app():
    logger.info('Getting application logs for sending as email for Denva')
    return jsonify(common_service.get_log_app(300))


@app.route("/log/app/recent")
def recent_log_app():
    logger.info('Getting recent application logs for sending as email for Denva')
    return jsonify(common_service.get_log_app(20))


@app.route("/log/hc")
def log_hc():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_hc(300))


@app.route("/log/hc/recent")
def recent_log_hc():
    logger.info('Getting recent healthcheck logs  for sending as email for Denva')
    return jsonify(common_service.get_log_ui(20))


@app.route("/log/ui")
def log_ui():
    logger.info('Getting server ui logs for Denva')
    return jsonify(common_service.get_log_ui(300))


@app.route("/log/ui/recent")
def recent_log_ui():
    logger.info('Getting recent server ui logs for sending as email  for Denva')
    return jsonify(common_service.get_log_ui(20))


@app.route("/hc")
def healthcheck():
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/")
def welcome():
    logger.info('Getting a main page')
    host = request.host_url[:-1]
    page_now = host + str(url_for('now'))
    page_system = host + str(url_for('system'))
    page_avg = host + str(url_for('average'))
    page_records = host + str(url_for('record'))
    page_stats = host + str(url_for('stats'))
    page_warns = host + str(url_for('today_warns'))
    page_warns_now = host + str(url_for('current_warns'))
    page_warns_count = host + str(url_for('count_warns'))
    page_recent_log_app = host + str(url_for('log_app'))
    page_recent_log_hc = host + str(url_for('log_hc'))
    data = {
        'page_now': page_now,
        'page_system': page_system,
        'page_avg': page_avg,
        'page_records': page_records,
        'page_stats': page_stats,
        'page_warns': page_warns,
        'page_warns_now': page_warns_now,
        'page_warns_count': page_warns_count,
        'page_recent_log_app': page_recent_log_app,
        'page_recent_log_hc': page_recent_log_hc
    }

    return render_template('dashboard.html', message=data)


if __name__ == '__main__':
    config_service.set_mode_to('denva')
    data_files.setup_logging('ui')
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
        healthcheck()
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email(APP_NAME,
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(exception))
        sys.exit(0)
