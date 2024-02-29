import logging
import sys
import traceback

from flask import Flask, jsonify, request

import config
import dom_utils
from emails import email_sender_service

config.EMAIL_PORT = 18010

app = Flask(__name__)
logger = logging.getLogger('app')
dom_utils.setup_test_logging('email')
APP_NAME = 'Server UI'


@app.route("/hc")
def healthcheck():
    return jsonify({"status": "OK",
                    "app": APP_NAME})


@app.route("/email/send", methods=['POST'])
def update_metrics_for():
    logger.info('Received request to send email')
    try:
        email_data = request.get_json(force=True)
        logger.debug(f'with body: {email_data}')
    except Exception as generic_exception:
        logger.error(f'Unable to generate json from request due to: {generic_exception}')
        return jsonify({"status": "ERROR"})

    response = email_sender_service.send_email_v2(email_data)
    # metrics_service.add(result['metrics'], result['result'])
    return jsonify({"status": "OK" if response else "FAILED"})


if __name__ == '__main__':

    logger.info('Starting web server')

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.run(host='0.0.0.0', debug=True, port=config.EMAIL_PORT)  # host added so it can be visible on local network
    except KeyboardInterrupt as keyboard_exception:
        print(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error(f'Something went badly wrong\n{exception}', exc_info=True)
        sys.exit(1)
    except BaseException as disaster:
        msg = f'Shit hit the fan and application died badly because {disaster}'
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
