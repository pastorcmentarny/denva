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
import traceback

from flask import Flask, jsonify, request

import config_service
from common import data_files
from denviro import enviro_service
from services import email_sender_service, common_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Denviro UI'


@app.route("/avg")
def average():
    logger.info('Getting average measurement from today')
    return jsonify(enviro_service.get_averages_for_today())


@app.route("/gc")
def gc():
    logger.info('Running GC..')
    return jsonify(common_service.run_gc())


@app.route("/halt")
def halt():
    logger.info('Stopping Denviro Pi')
    return jsonify(common_service.stop_device(APP_NAME))


@app.route("/hc")
def healthcheck():
    logger.info('performing healthcheck for Denviro')
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/log/app")
def log_app():
    logger.info('Getting application logs for sending as email for Denviro')
    return jsonify(common_service.get_log_app(300))


@app.route("/log/app/recent")
def recent_log_app():
    logger.info('Getting recent application logs for sending as email for Denviro')
    return jsonify(common_service.get_log_app(20))


@app.route("/log/count/app")
def log_count_app():
    logger.info('Getting recent healthcheck logs for sending as email for Denviro')
    return jsonify(common_service.get_log_count_for('app'))


@app.route("/log/count/ui")
def log_count_ui():
    logger.info('Getting recent healthcheck logs for sending as email for Denviro')
    return jsonify(common_service.get_log_count_for('ui'))


@app.route("/log/hc")
def log_hc():
    logger.info('Getting recent healthcheck logs for sending as email for Denviro')
    return jsonify(common_service.get_log_hc(300))


@app.route("/log/hc/recent")
def recent_log_hc():
    logger.info('Getting recent healthcheck logs  for sending as email for Denviro')
    return jsonify(common_service.get_log_ui(20))


@app.route("/log/ui")
def log_ui():
    logger.info('Getting server ui logs for Denviro')
    return jsonify(common_service.get_log_ui(300))


@app.route("/log/ui/recent")
def recent_log_ui():
    logger.info('Getting recent server ui logs for sending as email  for Denviro')
    return jsonify(common_service.get_log_ui(20))


@app.route("/now")
def now():
    logger.info('Getting current measurement from Denviro')
    return jsonify(enviro_service.get_last_measurement())


@app.route("/reboot")
def reboot():
    logger.info('Reboot Denviro UI')
    return jsonify(common_service.reboot_device())


@app.route("/report/yesterday")
def last_report():
    logger.info('Getting report for yesterday')
    return jsonify(enviro_service.get_report_for_yesterday())


@app.route("/records")
def record():
    logger.info('Getting record measurement from today')
    return jsonify(enviro_service.get_records_for_today())


@app.route("/system")
def system():
    logger.info('Getting system information about Denviro')
    return jsonify(common_service.get_system_info())


@app.route("/warns/now")
def current_warns():
    logger.debug('Getting current warnings for Denviro')
    return jsonify(enviro_service.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    logger.info('Getting warnings count for Denviro')
    return jsonify(enviro_service.get_current_warnings_count())


@app.route("/")
def get_measurement():
    logger.info('Getting current measurement')
    return jsonify(enviro_service.get_current_measurement(request.host_url[:-1]))


if __name__ == '__main__':
    config_service.set_mode_to('denviro')
    data_files.setup_logging('ui')
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email(APP_NAME,
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(exception))
        sys.exit(0)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
