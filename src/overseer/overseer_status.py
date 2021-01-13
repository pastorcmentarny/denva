"""
Two modes:
* auto - running default schedule
* manual - read file and do action
"""
import traceback
from datetime import datetime

import mote_lighting


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


if __name__ == '__main__':
    try:
        while True:
            mote_lighting.display_fasting_status()
            if is_night_mode():
                mote_lighting.night_mode()
            elif is_stand_up():
                mote_lighting.party_mode()
            elif is_busy_at_work():
                mote_lighting.red_alert()
            else:
                mote_lighting.daydream()
    except KeyboardInterrupt:
        print('Received request application to shut down.. goodbye!')
    except Exception as exception:
        print('Whoops. {}'.format(exception))
        traceback.print_exc()
