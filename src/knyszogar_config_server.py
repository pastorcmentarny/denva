"""
store config as file on each device
app on each service will try to pull new version of config every minute
if version diff then update it
if not then keep it old one
each app will use current
"""
import logging
import os
import sys
import traceback

from flask import Flask, jsonify

import config
import dom_utils
from services import common_service

logger = logging.getLogger('app')
dom_utils.setup_test_logging('config')

app = Flask(__name__)
APP_NAME = 'Knyszogar Config Service'

@app.route("/")
def get_main_route():
    return get_config()

@app.route("/config")
def get_config():
    logger.debug("get config")
    return config.load_cfg()

@app.route("/reload")
def reload_config():
    logger.debug("reload config from file")
    return config.reload_config_from_file()


@app.route("/hc")
def healthcheck():
    logger.debug("Sending heathcheck")
    return jsonify(common_service.get_healthcheck(APP_NAME))


if __name__ == '__main__':

    logger.info('Starting web server')

    try:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.config['JSON_AS_ASCII'] = False
        app.config['SECRET_KEY'] = os.urandom(24).hex()

        app.run(host='0.0.0.0',  port=18004, debug=False)  # host added so it can be visible on local network
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
