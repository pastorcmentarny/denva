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
from flask import Flask, jsonify, url_for, send_file, request, render_template

import app_server_service
import commands
import config_serivce
import data_files
import information_service
import local_data_gateway
import networkcheck
import report_service
import sensor_log_reader
import system_data_service
import tubes_train_service
import web_data

app = Flask(__name__)
logger = logging.getLogger('server')
APP_NAME = 'Server UI'


@app.route("/gateway")
def gateway_page():
    return render_template('gateway.html', message=app_server_service.get_gateway_data())


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_last_measurement())


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


@app.route("/report/yesterday")
def last_report_from_denva_and_enviro():
    return jsonify(report_service.get_reports_from_denva_and_enviro())


@app.route("/webcam")
def do_picture():
    filename = commands.capture_picture()
    return send_file(filename, mimetype='image/jpeg')


@app.route("/hc")
def healthcheck():
    return jsonify({"status": "UP",
                    "app": APP_NAME,
                    "network": networkcheck.network_check(config_serivce.get_options()['inChina'])})


@app.route("/ricky")
def ricky():
    return jsonify(information_service.get_data_about_rickmansworth())


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data.get_status()
    }
    return jsonify(tt_statuses)


@app.route("/system")
def system():
    logger.info('Getting information about system')
    return jsonify(system_data_service.get_system_information())


@app.route("/tt/delays")
def tt_delays_counter():
    return jsonify(tubes_train_service.count_tube_problems_today())


@app.route("/frame")
def frame():
    filename = app_server_service.get_random_frame()
    print(filename)
    return send_file(filename, mimetype='image/jpeg')


@app.route('/denva', methods=['POST'])
def store_denva_measurement():
    logging.info('processing denva measurement request')
    print(request.is_json)
    logger.info(request.get_json())
    print(request.get_json())
    return jsonify(success=True)


@app.route('/enviro', methods=['POST'])
def store_enviro_measurement():
    logging.info('processing enviro measurement request')
    print(request.is_json)
    logger.info(request.get_json())
    print(request.get_json())
    return jsonify(success=True)


@app.route("/")
def welcome():
    host = request.host_url[:-1]
    page_now = host + str(url_for('now'))
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_gateway = host + str(url_for('gateway_page'))
    page_ricky = host + str(url_for('ricky'))
    page_frame = host + str(url_for('frame'))
    page_webcam = host + str(url_for('do_picture'))
    data = {
        'page_now': page_now,
        'page_tube_trains': page_tube_trains,
        'page_tt_delays_counter': page_tt_delays_counter,
        'page_recent_log_app': page_recent_log_app,
        'page_frame': page_frame,
        'page_webcam': page_webcam,
        'page_ricky': page_ricky,
        'page_gateway': page_gateway,
        'warnings': local_data_gateway.get_current_warnings_for_all_services(),
        'denva': local_data_gateway.get_current_reading_for_denva(),
        'enviro': local_data_gateway.get_current_reading_for_enviro(),
        'system': app_server_service.get_current_system_information_for_all_services(),
        'links': app_server_service.get_links_for_gateway()
    }

    return render_template('dashboard-server.html', message=data)


if __name__ == '__main__':
    config_serivce.set_mode_to('server')
    data_files.setup_logging()
    logger.info('Starting web server')

    try:
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
        healthcheck()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        '''email_sender_service.send_error_log_email('web application',
                                                  'you may need reset web application as it looks like web app '
                                                  'crashes due to {}'.format(e))'''
        sys.exit(0)
