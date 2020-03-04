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
import networkcheck

import commands
import config_serivce
import data_files
import information_service
import report_service
import sensor_log_reader
import tubes_train_service
import web_data
import local_data_gateway

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Server UI'


@app.route("/gateway")
def gateway_page():
    return render_template('gateway.html', message=app_server_service.get_gateway_data())


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_last_measurement())


@app.route("/log/app")
def recent_log_app():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 300))


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
                    "app": APP_NAME})


@app.route("/ricky")
def ricky():
    return jsonify(information_service.get_data_about_rickmansworth())


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data.get_status()
    }
    return jsonify(tt_statuses)


@app.route("/tt/delays")
def tt_delays_counter():
    return jsonify(tubes_train_service.count_tube_problems_today())


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


def get_enviro_mocked_data():
    return {
        "temperature": '17.5*C',
        "pressure": '1030',
        "humidity": '39.51%',
        "light": '100',
        "proximity": '100',
        "oxidised": '100',
        "reduced": '100',
        "nh3": '100',
        "pm1": '100',
        "pm25": '100',
        "pm10": '100',
    }


@app.route("/")
def welcome():
    host = request.host_url[:-1]
    page_now = host + str(url_for('now'))
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_gateway = host + str(url_for('gateway_page'))
    page_ricky = host + str(url_for('ricky'))
    page_webcam = host + str(url_for('do_picture'))
    data = {
        'page_now': page_now,
        'page_tube_trains': page_tube_trains,
        'page_tt_delays_counter': page_tt_delays_counter,
        'page_recent_log_app': page_recent_log_app,
        'page_webcam': page_webcam,
        'page_ricky': page_ricky,
        'page_gateway': page_gateway,
        'warnings': local_data_gateway.get_current_warnings_for_all_services(),
        'denva': local_data_gateway.get_current_reading_for_denva(),
        'enviro': local_data_gateway.get_current_reading_for_enviro(),
        'network' : networkcheck.network_check(config_serivce.get_options()['inChina'])
    }

    return render_template('dashboard-server.html', message=data)


if __name__ == '__main__':
    data_files.setup_logging('dev')
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
