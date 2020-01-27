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
import averages
import commands
import data_files
import information_service
import records
import report_service
import sensor_log_reader
import sensor_warnings
import tubes_train_service
import web_data

app = Flask(__name__)
logger = logging.getLogger('app')
APP_NAME = 'Server UI'


@app.route("/stats")
def stats():
    return jsonify(sensor_log_reader.load_data_for_today())


@app.route("/records")
def record():
    return jsonify(records.get_records_for_today())


@app.route("/avg")
def average():
    return jsonify(averages.get_averages_for_today())


@app.route("/warns")
def warns_page():
    data = {}
    data['warnings'] = app_server_service.get_all_warnings_page()
    return render_template('warnings.html', message=data)


@app.route("/gateway")
def gateway_page():
    return render_template('gateway.html', message=app_server_service.get_gateway_data())


@app.route("/warns/today")
def today_warns():
    return jsonify(sensor_warnings.get_warnings_for_today())


@app.route("/warns/now")
def current_warns():
    return jsonify(sensor_warnings.get_current_warnings())


@app.route("/warns/count")
def count_warns():
    return jsonify(sensor_warnings.count_warning_today())


@app.route("/warns/date")
def specific_day_warns():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    return jsonify(sensor_warnings.get_warnings_for(year, month, day))


@app.route("/now")
def now():
    return jsonify(sensor_log_reader.get_last_measurement())


@app.route("/system")
def system():
    return jsonify(commands.get_system_info())


@app.route("/log/app")
def recent_log_app():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/logs.log', 300))


@app.route("/log/hc")
def recent_log_hc():
    return jsonify(commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 300))


@app.route("/report/yesterday")
def last_report():
    return jsonify(report_service.generate_for_yesterday())


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data.get_status()
    }
    return jsonify(tt_statuses)


@app.route("/tt/delays")
def tt_delays_counter():
    return jsonify(tubes_train_service.count_tube_problems_today())


@app.route("/tt/counter")
def tt_counter():
    return jsonify(tubes_train_service.count_tube_color_today())


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


def get_denva_mocked_data() -> dict:
    return {
        'timestamp': '2020-01-27',
        'temp': '17*C',
        'pressure': '1030',
        'humidity': '39.03',
        'gas_resistance': '123456789',
        'colour': '#00000',
        'aqi': 'n/a',
        'uva_index': '0.01',
        'uvb_index': '0.01',
        'motion': '95.08',
        'ax': '101',
        'ay': '102',
        'az': '103',
        'gx': '104',
        'gy': '105',
        'gz': '106',
        'mx': '107',
        'my': '108',
        'mz': '109',
        'cpu_temp': '45.08*C',
        'eco2': '400',
        'tvoc': '200'
    }


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
    page_system = host + str(url_for('system'))
    page_avg = host + str(url_for('average'))
    page_records = host + str(url_for('record'))
    page_stats = host + str(url_for('stats'))
    page_warns = host + str(url_for('today_warns'))
    page_warns_now = host + str(url_for('current_warns'))
    page_warns_count = host + str(url_for('count_warns'))
    page_last_report = host + str(url_for('last_report'))
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_tube_trains_counter = host + str(url_for('tt_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_recent_log_hc = host + str(url_for('recent_log_hc'))
    page_gateway = host + str(url_for('gateway_page'))
    page_ricky = host + str(url_for('ricky'))
    page_warns = host + str(url_for('ricky'))
    page_webcam = host + str(url_for('do_picture'))
    data = {
        'page_now': page_now,
        'page_system': page_system,
        'page_avg': page_avg,
        'page_records': page_records,
        'page_stats': page_stats,
        'page_warns': page_warns,
        'page_warns_now': page_warns_now,
        'page_warns_count': page_warns_count,
        'page_last_report': page_last_report,
        'page_tube_trains': page_tube_trains,
        'page_tt_delays_counter': page_tt_delays_counter,
        'page_tube_trains_counter': page_tube_trains_counter,
        'page_recent_log_app': page_recent_log_app,
        'page_recent_log_hc': page_recent_log_hc,
        'page_webcam': page_webcam,
        'page_ricky': page_ricky,
        'page_gateway': page_gateway,
        'page_warnings': warns_page,
        'denva': get_denva_mocked_data(),
        'enviro': get_enviro_mocked_data()
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
