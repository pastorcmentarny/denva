"""
Two modes:
* auto - running default schedule
* manual - read file and do action
"""
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path

import config_service
from common import data_files
from overseer import mote_lighting
from services import email_sender_service

EMPTY = ""

APP_NAME = 'overseer'
MODE_BORG = 'borg'
MODE_RAIN = 'rain'
MODE_DREAM = 'dream'
MODE_PARTY = 'party'
MODE_YELLOW_COLOR = 'yellow'
MODE_RED_COLOR = 'red'
MODE_LIGHT_OFF = 'light_off'
MODE_FIRE_LIGHTING = 'fire'

logger = logging.getLogger(APP_NAME)


def is_busy_at_work():
    return datetime.now().isoweekday() < 6 and (16 > datetime.now().hour >= 8)


def is_default_fasting_time() -> bool:
    return datetime.now().hour > 18 or datetime.now().hour <= 12


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def is_do_not_disturb() -> bool:
    return True


def is_stand_up() -> bool:
    if datetime.now().isoweekday() < 6 and (datetime.now().hour == 9 and (59 >= datetime.now().minute >= 40)):
        return True
    else:
        return False


modes = [MODE_RED_COLOR, MODE_YELLOW_COLOR, MODE_PARTY, MODE_DREAM, MODE_RAIN, MODE_BORG, MODE_LIGHT_OFF,
         MODE_FIRE_LIGHTING]


def override_mode() -> str:
    status_file = Path(r"D:\overseer_mode.txt")  # config_service.get_overseer_mode_file_path())
    try:
        f = open(status_file)
        result = f.read()
        logger.info(f'mode:{result}')
        if result:
            return result.strip()
        else:
            return EMPTY
    except Exception as an_exception:
        logger.error(f'Unable to read override mode from file due to :{an_exception}', exc_info=True)
        return EMPTY


def is_in_override(a_mode):
    return a_mode in modes


def set_manual_mode(manual_mode):
    logger.info(f'Setting mode to {manual_mode}')
    if manual_mode == MODE_RED_COLOR:
        mote_lighting.red_alert()
    elif manual_mode == MODE_YELLOW_COLOR:
        mote_lighting.yellow_alert()
    elif manual_mode == MODE_DREAM:
        mote_lighting.daydream()
    elif manual_mode == MODE_RAIN:
        mote_lighting.rain()
    elif manual_mode == MODE_BORG:
        mote_lighting.borg()
    elif manual_mode == MODE_FIRE_LIGHTING:
        mote_lighting.fire_effect_with_lighting()
    elif manual_mode == MODE_LIGHT_OFF:
        mote_lighting.turn_light_off()
    else:
        logger.warning(f'WARNING! Unknown mode: {manual_mode}')


def app_loop():
    counter = 0
    while True:
        counter += 1
        print(f'counter: {counter}')
        mode = override_mode()
        if is_in_override(mode):
            set_manual_mode(mode)
        else:
            if is_night_mode():
                mote_lighting.night_mode()
            elif is_stand_up():
                mote_lighting.party_mode()
            elif is_busy_at_work():
                mote_lighting.red_alert()
            else:
                mote_lighting.daydream()


if __name__ == '__main__':
    config_service.set_mode_to(APP_NAME)
    data_files.setup_logging(APP_NAME)
    logger.info('Starting application ... \n Press Ctrl+C to shutdown')
    try:
        app_loop()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        sys.exit(0)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email(APP_NAME,
                                                  '{} crashes due to {}'.format(APP_NAME, exception))
    except BaseException as disaster:
        logger.error('Something went badly wrong\n{}'.format(disaster), exc_info=True)
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
