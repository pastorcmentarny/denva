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
from flask import Flask, jsonify, request
import averages
import commands
import data_files
import email_sender_service
import sensor_log_reader
import networkcheck
import config_serivce
import sensor_warnings

app = Flask(__name__)
logger = logging.getLogger('server')
APP_NAME = 'Denva Enviro UI'

@app.route("/avg")
def average():
    logger.info('Getting average measurement from today')
    return jsonify(averages.get_enviro_averages_for_today())

@app.route("/now")
def now():
    logger.info('Getting current measurement from Enviro')
    return jsonify(sensor_log_reader.get_last_enviro_measurement())


@app.route("/system")
def system():
    logger.info('Getting system information about Enviro')
    return jsonify(commands.get_system_info())


@app.route("/log/app")
def log_app():
    logger.info('Getting application logs for sending as email for Enviro')
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 300))


@app.route("/log/app/recent")
def recent_log_app():
    logger.info('Getting recent application logs for sending as email for Enviro')
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 20))


@app.route("/log/hc")
def log_hc():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 300))


@app.route("/log/hc/recent")
def recent_log_hc():
    logger.info('Getting recent healthcheck logs  for sending as email for Enviro')
    return jsonify(commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 20))


@app.route("/log/ui")
def log_ui():
    logger.info('Getting server ui logs for Enviro')
    return jsonify(commands.get_lines_from_path('/home/pi/logs/server.log', 300))


@app.route("/log/ui/recent")
def recent_log_ui():
    logger.info('Getting recent server ui logs for sending as email  for Enviro')
    return jsonify(commands.get_lines_from_path('/home/pi/logs/server.log', 20))


@app.route("/warns/now")
def current_warns():
    logger.debug('Getting current warnings for Enviro')
    return jsonify(sensor_warnings.get_current_warnings_for_enviro())

@app.route("/warns/count")
def count_warns():
    logger.info('Getting warnings count for Enviro')
    return jsonify(sensor_warnings.count_warning_today())

@app.route("/hc")
def healthcheck():
    return jsonify({"status": "UP",
                    "app": APP_NAME,
                    "network": networkcheck.network_check(config_serivce.get_options()['inChina'])})


@app.route("/")
def get_measurement():
    measurement = sensor_log_reader.get_last_enviro_measurement()
    measurement['host'] = request.host_url[:-1]
    measurement['system'] = commands.get_system_info()
    return jsonify(measurement)


if __name__ == '__main__':
    config_serivce.set_mode_to('enviro')
    data_files.setup_logging()
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email('web application',
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(e))
        sys.exit(0)
