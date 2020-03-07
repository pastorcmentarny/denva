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

import commands
import data_files
import email_sender_service
import sensor_log_reader
import networkcheck
import config_serivce

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Denva Enviro UI'


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_last_enviro_measurement())


@app.route("/system")
def system():
    return jsonify(commands.get_system_info())


@app.route("/log/app")
def recent_log_app():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 300))


@app.route("/log/hc")
def recent_log_hc():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/enviro-hc.log', 300))


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
    data_files.setup_logging('enviro')
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email('web application',
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(e))
        sys.exit(0)
