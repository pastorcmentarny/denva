import logging
import sys
import traceback

from flask import Flask, jsonify, request

import dom_utils
from emails import email_sender_service

app = Flask(__name__)
logger = logging.getLogger('app')
dom_utils.setup_test_logging('healthcheck')
APP_NAME = 'Server UI'


@app.route("/hc")
def healthcheck():
    return jsonify({"status": "UP",
                    "app": APP_NAME})


@app.route("/email/send", methods=['POST'])
def update_metrics_for():
    logger.info('Received request to send email')
    try:
        email_data = request.get_json(force=True)
        logger.debug('with body: {}'.format(email_data))
    except Exception as generic_exception:
        logger.error(f'Unable to generate json from request due to: {generic_exception}')
        return jsonify({"status": "ERROR"})

    response = email_sender_service.send_email_v2(email_data)
    # metrics_service.add(result['metrics'], result['result'])
    return jsonify({"status": "OK" if response else "FAILED"})


if __name__ == '__main__':

    dom_utils.setup_test_logging('email')

    logger.info('Starting web server')

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True, port=18010)  # host added so it can be visible on local network
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
