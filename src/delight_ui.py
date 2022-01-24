#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging
import sys
import traceback

from flask import Flask, jsonify, request

from common import data_files
from delight import delight_service
from services import common_service
from email import email_sender_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Denva Delight UI'


@app.route("/flights/today")
def flights_today():
    logger.info('Getting flights detected today')
    return jsonify(delight_service.get_flights_for_today())


@app.route("/flights/yesterday")
def flights_yesterday():
    logger.info('Getting flights detected yesterday')
    return jsonify(delight_service.get_flights_for_yesterday())


@app.route("/gc")
def gc():
    logger.info('Running GC for {}'.format(APP_NAME))
    return jsonify(delight_service.run_gc())


@app.route("/halt")
def halt():
    logger.info('Stopping Denviro Pi')
    return jsonify(common_service.stop_device(APP_NAME))


@app.route("/hc")
def healthcheck():
    logger.info('performing healthcheck for {}'.format(APP_NAME))
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/shc/update", methods=['POST'])
def update_system_healthcheck_for():
    logger.info('updating device status to {}'.format(request.get_json(force=True)))
    delight_service.update_hc_for(request.get_json(force=True))
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/shc/get")
def get_system_healthcheck_for():
    logger.info('updating healthcheck')
    return jsonify(delight_service.get_system_hc())


@app.route("/log/count/app")
def log_count_app():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_for('app'))


@app.route("/log/count/ui")
def log_count_ui():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_for('ui'))


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


@app.route("/reboot")
def reboot():
    logger.info('Reboot Delight UI')
    return jsonify(common_service.reboot_device())


@app.route("/system")
def system():
    logger.info('Getting system information for {}'.format(APP_NAME))
    return jsonify(delight_service.get_system_info())


@app.route("/")
def get_measurement():
    return jsonify(delight_service.get_flights_for_today())


# TODO improve it
@app.route("/test")
def get_ping_test():
    logger.info("Running ping test")
    return jsonify(delight_service.get_ping_test_results())


if __name__ == '__main__':
    config_service.set_mode_to('delight')
    data_files.setup_logging('ui')
    delight_service.reset_hc()
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True)
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
