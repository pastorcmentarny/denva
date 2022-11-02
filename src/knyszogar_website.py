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
import datetime
import logging
import sys
import traceback

from flask import Flask, jsonify, url_for, request, render_template

import config
import dom_utils
from gateways import web_data_gateway
from server import app_server_service, server_storage_service
from server import delight_service
from server import healthcheck_service
from services import common_service, diarist_service
from services import information_service, text_service, metrics_service

app = Flask(__name__)
logger = logging.getLogger('www')
dom_utils.setup_test_logging('website', False)
APP_NAME = 'Knyszogar Website'


@app.route("/metrics/add", methods=['POST'])
def update_metrics_for():
    logger.info('Updating metrics {}'.format(request.get_json(force=True)))
    result = request.get_json(force=True)
    metrics_service.add(result['metrics'], result['result'])
    return jsonify({"status": "OK"})


@app.route("/hc")
def healthcheck():
    logger.debug("Sending heathcheck")
    return jsonify(common_service.get_healthcheck(APP_NAME))


@app.route("/shc/update", methods=['POST'])
def update_system_healthcheck_for():
    logger.info('Updating device application status to {}'.format(request.get_json(force=True)))
    healthcheck_service.update_for(request.get_json(force=True))
    return jsonify({})


@app.route("/shc/change", methods=['POST'])
def update_device_to_on_off_for():
    logger.info('Updating device power state to {}'.format(request.get_json(force=True)))
    healthcheck_service.update_device_power_state_for(request.get_json(force=True))
    return jsonify({})


@app.route("/device/status/update", methods=['POST'])
def update_device_status_for():
    logger.info('Updating device status to {}'.format(request.get_json(force=True)))
    healthcheck_service.update_device_status_for(request.get_json(force=True))
    return jsonify({})


@app.route("/measurement/denva", methods=['POST'])
def update_denva_measurement():
    logger.info('Updating denva measurement. Data size {}'.format(len(str(request.get_json(force=True)))))
    server_storage_service.save_denva_measurement(request.get_json(force=True))
    return jsonify({})


@app.route("/measurement/denviro", methods=['POST'])
def update_denviro_measurement():
    logger.info('Updating denviro measurement. Data size {}'.format(len(str(request.get_json(force=True)))))
    server_storage_service.save_denva_measurement(request.get_json(force=True))
    return jsonify({})


@app.route("/measurement/trases", methods=['POST'])
def update_trases_measurement():
    logger.info('Updating trases measurement. Data size {}'.format(len(str(request.get_json(force=True)))))
    server_storage_service.save_trases_measurement(request.get_json(force=True))
    return jsonify({})


@app.route("/diary/add", methods=['POST'])
def add_diary():
    logger.info('Add entry to diary. Data size {}'.format(len(str(request.get_json(force=True)))))
    diarist_service.add(request.get_json(force=True))
    return jsonify({})


@app.route('/forty')
def yearly_goals():
    return render_template('40b440.html')


@app.route('/stop-all')
def stop_all_devices():
    logging.info('Stopping all PI devices.')
    return jsonify(app_server_service.stop_all_devices(config.load_cfg()))


@app.route('/reboot-all')
def reboot_all_devices():
    logging.info('Rebooting all PI devices.')
    return jsonify(app_server_service.reboot_all_devices(config.load_cfg()))


@app.route("/gc")
def gc():
    logger.info('Running GC..')
    return jsonify(app_server_service.run_gc())


@app.route("/log/count/app")
def log_count_app():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_from_path('app'))


# FIXME does not work
@app.route("/log/count/display")
def log_count_display():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_from_path('display'))


@app.route("/log/count/email")
def log_count_email():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_from_path('email'))


@app.route("/log/count/hc")
def log_count_hc():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_from_path('healthcheck'))


@app.route("/log/count/www")
def log_count_www():
    logger.info('Getting recent healthcheck logs for sending as email for Denva')
    return jsonify(common_service.get_log_count_from_path('website'))


@app.route("/metrics/get")
def get_metrics():
    logger.info('getting current metrics')
    return jsonify(metrics_service.get_currents_metrics())


@app.route("/report/yesterday")
def get_report_from_yesterday():
    return jsonify(app_server_service.get_report_for_yesterday())


@app.route("/ricky")
def ricky():
    return jsonify(information_service.get_data_about_rickmansworth())


@app.route("/system")
def system():
    logger.info('Getting information about system')
    result = common_service.get_system_info()
    return jsonify(result)


@app.route("/text")
def get_text():
    return text_service.get_text_to_display()


@app.route("/tt")
def tube_trains_status():
    tt_statuses = {
        "Train & Trains": web_data_gateway.get_status()
    }
    return jsonify(tt_statuses)


@app.route('/tt/stats')
def tt_delay_stats():
    data = app_server_service.count_tube_problems_today()
    return render_template('tube.html', message=data)


@app.route("/trases/off")
def trases_off():
    app_server_service.set_trases_to_off()
    return jsonify('{"device":  false}')


@app.route("/trases/off")
def trases_on():
    app_server_service.set_trases_to_on()
    return jsonify('{"device":  true}')


@app.route("/status")
def status():
    start = datetime.datetime.now()

    device_status_data = app_server_service.get_device_status(config.load_cfg())

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
    page_tt_delays_counter = host + str(url_for('tt_delay_stats'))
    page_ricky = host + str(url_for('ricky'))
    data = app_server_service.get_data_for_page(config.load_cfg(), page_ricky,
                                                page_tt_delays_counter, page_tube_trains)
    data.update()
    extra_data = app_server_service.get_gateway_data()
    all_data = dict(data)
    all_data.update(extra_data)

    stop = datetime.datetime.now()

    delta = stop - start
    time = int(delta.total_seconds() * 1000)
    logger.info(f'It took {time} ms.')
    return render_template('hq.html', message=all_data)


# FIXME
@app.route("/flights/today")
def flights_today():
    logger.info('Getting flights detected today')
    return jsonify(delight_service.get_flights_for_today())


# FIXME
@app.route("/flights/yesterday")
def flights_yesterday():
    logger.info('Getting flights detected yesterday')
    return jsonify(delight_service.get_flights_for_yesterday())


@app.route("/halt")
def halt():
    logger.info('Stopping Server Pi')
    return jsonify(common_service.stop_device(APP_NAME))


@app.route("/shc/get")
def get_system_healthcheck_for():
    logger.info('updating healthcheck')
    return jsonify(delight_service.get_system_hc())


@app.route("/reboot")
def reboot():
    logger.info('Reboot Server')
    return jsonify(common_service.reboot_device())


@app.route("/now-next")
def get_now_and_next_event():
    logger.info('Getting now and next event on daily')
    return jsonify(app_server_service.get_now_and_next_event())


@app.route("/")
def get_measurement():
    return hq()


# TODO improve it
@app.route("/ping")
def get_ping_test():
    logger.info("Running ping test")
    return jsonify(delight_service.get_ping_test_results())


if __name__ == '__main__':

    logger.info('Starting web server')

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True)  # host added so it can be visible on local network
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
