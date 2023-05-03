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
import traceback

from flask import Flask, jsonify, request


import dom_utils
from common import commands
from denva import denva2_service
from services import common_service
from emails import email_sender_service

app = Flask(__name__)
logger = logging.getLogger('app')
dom_utils.setup_logging('ui', True)

APP_NAME = 'Denva TW0 UI'


@app.route("/avg")
def average():
    logger.info('Getting average measurement from today')
    return jsonify(denva2_service.get_averages())


@app.route("/halt")
def halt():
    logger.info('Stopping Denva TWO')
    return jsonify(common_service.stop_device(APP_NAME))


@app.route("/hc")
def healthcheck():
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/log/system")
def recent_system_log_app():
    logger.info('Getting system logs')
    return jsonify(commands.get_system_logs(200))


@app.route("/log/count/app")
def log_count_app():
    logger.info('Getting recent healthcheck logs for sending as email for Denva TWO')
    return jsonify(common_service.get_log_count_for('app'))


@app.route("/log/count/ui")
def log_count_ui():
    logger.info('Getting recent healthcheck logs for sending as email for Denva TWO')
    return jsonify(common_service.get_log_count_for('ui'))


@app.route("/now")
def now():
    logger.info('Getting last measurement')
    return jsonify(denva2_service.get_last_measurement_from_all_sensors())


@app.route("/report/yesterday")
def last_report():
    logger.info('Getting report for yesterday')
    return jsonify(denva2_service.get_last_report())


@app.route("/reboot")
def reboot():
    logger.info('Rebooting device')
    return jsonify(common_service.reboot_device())


@app.route("/records")
def records():
    logger.info('Getting record measurement from today')
    return jsonify(denva2_service.get_records_for_today())


# FIXME
@app.route("/stats")
def stats():
    logger.info('Get all stats for today')
    return jsonify(denva2_service.get_all_stats_for_today())


@app.route("/system")
def system():
    logger.info('Getting information about system')
    return jsonify(common_service.get_system_info())


@app.route("/warns")
def today_warns():
    logger.info('Getting all warnings from today')
    return jsonify(denva2_service.get_warnings_for_today())


@app.route("/warns/now")
def current_warns():
    logger.info('Getting current warnings')
    return jsonify(denva2_service.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    logger.info('Getting warnings count')
    return jsonify(denva2_service.count_warnings())


@app.route("/warns/date")
def specific_day_warns():
    args = request.args
    year = args.get('year')
    month = args.get('month')
    day = args.get('day')
    logger.info('Getting warnings for {}.{}.{}'.format(day, month, year))
    return jsonify(denva2_service.get_warnings_for(year, month, day))


@app.route("/")
def last_measurement():
    return jsonify(denva2_service.get_last_measurement_from_all_sensors())


if __name__ == '__main__':
    logger.info('Starting web server for {}'.format(APP_NAME))

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
        healthcheck()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email(APP_NAME,
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(exception))
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
