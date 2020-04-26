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
from flask import Flask, jsonify

import config_service
from common import data_files
from delight import delight_service
from services import common_service, email_sender_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Denva Delight UI'


@app.route("/gc")
def gc():
    logger.info('Running GC for {}'.format(APP_NAME))
    return jsonify(delight_service.run_gc())


@app.route("/hc")
def healthcheck():
    logger.info('performing healthcheck for {}'.format(APP_NAME))
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/log/app")
def log_app():
    logger.info('Getting application logs for sending as email for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_app(300))


@app.route("/log/app/recent")
def recent_log_app():
    logger.info('Getting recent application logs for sending as email for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_app(20))


@app.route("/log/hc")
def log_hc():
    logger.info('Getting recent healthcheck logs for sending as email for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_hc(300))


@app.route("/log/hc/recent")
def recent_log_hc():
    logger.info('Getting recent healthcheck logs  for sending as email  for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_ui(20))


@app.route("/log/ui")
def log_ui():
    logger.info('Getting server ui logs for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_ui(300))


@app.route("/log/ui/recent")
def recent_log_ui():
    logger.info('Getting server ui logs for {}'.format(APP_NAME))
    return jsonify(delight_service.get_log_ui(20))


@app.route("/system")
def system():
    logger.info('Getting system information for {}'.format(APP_NAME))
    return jsonify(delight_service.get_system_info())


@app.route("/")
def get_measurement():
    return jsonify({
        'mode': 'work in progress',
        'counter': 0
    })


if __name__ == '__main__':
    config_service.set_mode_to('delight')
    data_files.setup_logging()
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email(APP_NAME,
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(e))
        sys.exit(0)
