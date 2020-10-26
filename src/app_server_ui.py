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

import config_service
from common import data_files
from gateways import web_data_gateway
from denvapa import app_server_service, webcam_service
from reports import report_service
from services import email_sender_service, information_service, tubes_train_service, system_data_service

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Server UI'


@app.route('/08r/add')  # example: http://192.168.0.200:5000/08r/add?race=59.59.9--1.1.2068--1--260
def add_result():
    result = request.args.get('race')
    logging.info('Processing enviro measurement request with race info: {}'.format(result))
    return jsonify(app_server_service.add_result(result))


@app.route('/08r/hst')
def get_08r_top10_time():
    logging.info('Getting top10 from ZeroEight track leaderboard')
    return jsonify(app_server_service.get_top_10())


@app.route('/08r/hss')
def get_08r_top10_score():
    logging.info('Getting top10 from ZeroEight track leaderboard')
    return jsonify(app_server_service.get_top_10_score())


@app.route('/all')
def get_all_08r_results():
    logging.info('Getting top10 from ZeroEight track leaderboard')
    return jsonify(app_server_service.get_all_results())


@app.route('/denva', methods=['POST'])
def store_denva_measurement():
    logging.info('Processing denva measurement request with json: {}'.format(request.get_json()))
    return jsonify(success=True)


@app.route('/enviro', methods=['POST'])
def store_enviro_measurement():
    logging.info('Processing enviro measurement request with json: {}'.format(request.get_json()))
    return jsonify(success=True)


@app.route("/frame")
def frame():
    logger.info('Requesting random picture')
    filename = app_server_service.get_random_frame()
    logger.info('Displaying {}'.format(filename))
    return send_file(filename, mimetype='image/jpeg')


@app.route("/gateway")
def gateway_page():
    return render_template('gateway.html', message=app_server_service.get_gateway_data())


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


@app.route("/hq") # prototype
def hq():
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

    extra_data = app_server_service.get_gateway_data()
    all_data = dict(data)
    all_data.update(extra_data)
    return render_template('hq.html', message=all_data)


@app.route("/")
def welcome():
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
    return render_template('dashboard-server.html', message=data)


if __name__ == '__main__':
    config_service.set_mode_to('server')
    data_files.setup_logging('ui')
    logger.info('Starting web server')

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
        healthcheck()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email('Mothership UI',
                                                  'Mothership UI crashes due to {}'.format(e))
        sys.exit(1)
