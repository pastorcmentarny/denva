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
import datetime
import logging
import sys
import traceback

from flask import Flask, jsonify, url_for, send_file, request, render_template

import config_service
from common import data_files
from denvapa import app_server_service, webcam_service
from gateways import web_data_gateway
from reports import report_service
from services import email_sender_service, information_service, tubes_train_service, system_data_service, text_service, \
    metrics_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Server UI'


# TODO do I need it?
@app.route('/denva', methods=['POST'])
def store_denva_measurement():
    logging.info('Processing denva measurement request with json: {}'.format(request.get_json()))
    return jsonify(success=True)


@app.route('/stop-all')
def stop_all_devices():
    logging.info('Stopping all PI devices.')
    return jsonify(app_server_service.stop_all_devices())


@app.route('/reboot-all')
def reboot_all_devices():
    logging.info('Rebooting all PI devices.')
    return jsonify(app_server_service.reboot_all_devices())


# TODO do I need it?
@app.route('/enviro', methods=['POST'])
def store_enviro_measurement():
    logging.info('Processing enviro measurement request with json: {}'.format(request.get_json()))
    return jsonify(success=True)


@app.route("/focus")
def focus():
    return render_template('focus.html', message={})


@app.route("/frame")
def frame():
    logger.info('Requesting random picture')
    filename = app_server_service.get_random_frame()
    logger.info('Displaying {}'.format(filename))
    return send_file(filename, mimetype='image/jpeg')


@app.route("/gc")
def gc():
    logger.info('Running GC..')
    return jsonify(app_server_service.run_gc())


@app.route("/hc")
def healthcheck():
    return jsonify({"status": "UP", "app": APP_NAME})


@app.route("/log/app")
def log_app():
    logger.info('Getting application logs')
    return jsonify(app_server_service.get_last_logs_for('logs.log', 300))


@app.route("/log/app/recent")
def recent_log_app():
    logger.info('Getting recent application logs for sending as email')
    return jsonify(app_server_service.get_last_logs_for('logs.log', 20))


@app.route("/log/hc")
def log_hc():
    logger.info('Getting healthcheck logs')
    return jsonify(app_server_service.get_last_logs_for('healthcheck.log', 300))


@app.route("/log/hc/recent")
def recent_log_hc():
    logger.info('Getting recent healthcheck logs for sending as email')
    return jsonify(app_server_service.get_last_logs_for('healthcheck.log', 20))


@app.route("/log/ui")
def log_ui():
    logger.info('Getting server ui logs')
    return jsonify(app_server_service.get_last_logs_for('server.log', 300))


@app.route("/log/ui/recent")
def recent_log_ui():
    logger.info('Getting recent server ui logs for sending as email')
    return jsonify(app_server_service.get_last_logs_for('server.log', 20))


@app.route("/metrics/add", methods=['POST'])
def update_metrics_for():
    logger.info('updating metrics {}'.format(request.get_json(force=True)))
    result = request.get_json(force=True)
    metrics_service.add(result['metrics'], result['result'])
    return jsonify({"status": "OK"})


@app.route("/metrics/get")
def get_metrics():
    logger.info('getting current metrics')
    return jsonify(metrics_service.get_currents_metrics())


@app.route("/report/yesterday")
def last_report_from_denva_and_enviro():
    return jsonify(report_service.get_yesterday_report_from_server())


@app.route("/report/diff")
def report_comparison_for_last_two_days():
    return jsonify(report_service.get_last_two_days_report_difference())


@app.route("/ricky")
def ricky():
    return jsonify(information_service.get_data_about_rickmansworth())


@app.route("/system")
def system():
    logger.info('Getting information about system')
    return jsonify(system_data_service.get_system_information())


@app.route("/text")
def get_text():
    return text_service.get_text_to_display()


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data_gateway.get_status()
    }
    return jsonify(tt_statuses)


@app.route("/tt/delays")
def tt_delays_counter():
    return jsonify(tubes_train_service.count_tube_problems_today())


@app.route("/webcam")
def do_picture():
    filename = webcam_service.capture_picture()
    return send_file(filename, mimetype='image/jpeg')


@app.route("/status")
def hq():
    start = datetime.datetime.now()

    device_status_data = app_server_service.get_device_status()

    stop = datetime.datetime.now()

    delta = stop - start
    time = int(delta.total_seconds() * 1000)
    logger.info(f'It took {time} ms to collect all data for device status.')
    return render_template('status.html', message=device_status_data)


@app.route("/hq")
def hq():
    start = datetime.datetime.now()

    host = request.host_url[:-1]
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_gateway = host + str(url_for('gateway_page'))
    page_ricky = host + str(url_for('ricky'))
    page_frame = host + str(url_for('frame'))
    page_webcam = host + str(url_for('do_picture'))
    data = app_server_service.get_data_for_page(page_frame, page_gateway, page_recent_log_app, page_ricky,
                                                page_tt_delays_counter, page_tube_trains, page_webcam)
    data.update()
    extra_data = app_server_service.get_gateway_data()
    all_data = dict(data)
    all_data.update(extra_data)

    stop = datetime.datetime.now()

    delta = stop - start
    time = int(delta.total_seconds() * 1000)
    logger.info(f'It took {time} ms.')
    return render_template('hq.html', message=all_data)


@app.route("/")
def welcome():
    return hq()  # redirect


if __name__ == '__main__':
    config_service.set_mode_to('server')
    data_files.setup_logging('ui')
    logger.info('Starting web server')

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
        email_sender_service.send_error_log_email('Mothership UI',
                                                  'Mothership UI crashes due to {}'.format(exception))
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
