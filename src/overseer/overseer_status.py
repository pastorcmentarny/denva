"""
Two modes:
* auto - running default schedule
* manual - read file and do action
"""
import traceback
from datetime import datetime
from pathlib import Path

import config_service
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


modes = ['red', 'yellow', 'party', 'dream']


def override_mode() -> str:
    status_file = Path(config_service.get_overseer_mode_file_path())
    try:
        f = open(status_file)
        result = f.read()
        if result:
            return result.strip()
        else:
            return ""
    except Exception as e:
        print(e)
        return ""


def is_in_override(a_mode):
    return a_mode in modes


def set_manual_mode(a_mode):
    print()
    if a_mode == 'red':
        mote_lighting.red_alert()
    elif a_mode == 'yellow':
        mote_lighting.yellow_alert()
    elif a_mode == 'dream':
        mote_lighting.daydream()
    else:
        print(f'WARNING! Unknown mode: {a_mode}')


if __name__ == '__main__':
    counter = 0
    try:
        while True:
            counter += 1
            print(f'counter: {counter}')
            if counter % 5 == 0:
                mote_lighting.display_fasting_status()
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
    except KeyboardInterrupt:
        print('Received request application to shut down.. goodbye!')
    except Exception as exception:
        print('Whoops. {}'.format(exception))
        traceback.print_exc()
