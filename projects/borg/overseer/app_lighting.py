"""
Two modes:
* auto - running default schedule
* manual - read file and do action
"""
import logging
import sys
import traceback
from datetime import datetime
from datetime import date
from pathlib import Path
import mote_lighting

EMPTY = ""

APP_NAME = 'Overseer (Borg)'
MODE_BORG = 'borg'
MODE_RAIN = 'rain'
MODE_DREAM = 'dream'
MODE_PARTY = 'party'
MODE_YELLOW_COLOR = 'yellow'
MODE_RED_COLOR = 'red'
MODE_LIGHT_OFF = 'light_o qff'
MODE_FIRE_LIGHTING = 'fire'
MODE_ORANGE_LIGHTING = 'orange'
MODE_NIGHT = 'night'

logger = logging.getLogger(MODE_BORG)


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


def is_lunch_break():
    if datetime.now().isoweekday() < 6 and datetime.now().hour == 12:
        return True
    else:
        return False


modes = [MODE_RED_COLOR, MODE_YELLOW_COLOR, MODE_PARTY, MODE_DREAM, MODE_RAIN, MODE_BORG, MODE_LIGHT_OFF,
         MODE_FIRE_LIGHTING, MODE_ORANGE_LIGHTING, MODE_NIGHT]


def override_mode() -> str:
    status_file = Path(r"/home/dom/overseer_mode.txt")  # config.get_overseer_mode_file_path())
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
    elif manual_mode == MODE_ORANGE_LIGHTING:
        mote_lighting.orange_lighting()
    elif manual_mode == MODE_NIGHT:
        mote_lighting.night_mode()
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
                mote_lighting.party_random_color_mode()
            elif is_lunch_break():
                mote_lighting.lunch_effect()
            elif is_busy_at_work():
                mote_lighting.red_alert()
            else:
                mote_lighting.borg()


def setup_test_logging(app_name: str):
    logging_level = logging.DEBUG
    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'/home/dom/data/logs/{app_name}-{date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.debug('logging setup complete')


if __name__ == '__main__':
    setup_test_logging('overseer')
    logger.info('Starting application ... \n Press Ctrl+C to shutdown')
    try:
        app_loop()
    except KeyboardInterrupt as keyboard_exception:
        print(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        sys.exit(0)
    except Exception as exception:
        logger.error(f'Something went badly wrong\n{exception}', exc_info=True)
    except BaseException as disaster:
        logger.error(f'Something went badly wrong\n{disaster}', exc_info=True)
        msg = f'Shit hit the fan and application died badly because {disaster}'
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
