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

from flask import Flask, jsonify, request, render_template, url_for

import dom_utils
from server import healthcheck_service, app_server_service  # , app_server_service

app = Flask(__name__)
logger = logging.getLogger('www')
APP_NAME = 'Server UI'


@app.route("/metrics/add", methods=['POST'])
def update_metrics_for():
    logger.info('updating metrics {}'.format(request.get_json(force=True)))
    result = request.get_json(force=True)
    logger.debug(result)
    # metrics_service.add(result['metrics'], result['result'])
    return jsonify({"status": "OK"})


# TODO use commons
@app.route("/hc")
def healthcheck():
    logger.debug("Sending heathcheck")
    return jsonify({"status": "UP",
                    "app": APP_NAME})


@app.route("/shc/update", methods=['POST'])
def update_system_healthcheck_for():
    logger.info('updating device status to {}'.format(request.get_json(force=True)))
    healthcheck_service.update_for(request.get_json(force=True))
    return jsonify({})


@app.route('/forty')
def yearly_goals():
    return render_template('40b440.html')



@app.route("/hq")
def hq():
    start = time.perf_counter()

    host = request.host_url[:-1]
    page_tube_trains = host + str(url_for('tube_trains_status'))
    page_tt_delays_counter = host + str(url_for('tt_delays_counter'))
    page_recent_log_app = host + str(url_for('recent_log_app'))
    page_ricky = host + str(url_for('ricky'))
    page_frame = host + str(url_for('frame'))
    page_webcam = host + str(url_for('do_picture'))
    data = app_server_service.get_data_for_page(page_frame, page_recent_log_app, page_ricky,
                                                page_tt_delays_counter, page_tube_trains, page_webcam)
    data.update()
    extra_data = app_server_service.get_gateway_data()
    all_data = dict(data)
    all_data.update(extra_data)

    stop = time.perf_counter()

    delta = stop - start
    time = int(delta.total_seconds() * 1000)
    logger.info(f'It took {time} ms.')
    return render_template('hq.html', message=all_data)


if __name__ == '__main__':

    dom_utils.setup_test_logging('website')

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
        """
        email_sender_service.send_error_log_email('Mothership UI',
                                                  'Mothership UI crashes due to {}'.format(exception))
        """
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
