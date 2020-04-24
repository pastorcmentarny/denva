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

from timeit import default_timer as timer

import sys
import time

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559

    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from subprocess import PIPE, Popen

import logging
from denva import cl_display
import config_service
from common import data_files, commands
# from denviro import denviro_display //FIXME fix issue with font loading,but I don't use display now
from services import email_sender_service
from services import sensor_warnings_service

logger = logging.getLogger('app')

bme280 = BME280()
pms5003 = PMS5003()

message = ""
top_pos = 25
factor = 0.8
delay = 0.5  # Debounce the proximity tap
mode = 0  # The starting mode
last_page = 0
light = 1
values = {}
temps = []
cpu_temps = []
cycle = 0
on = True


def get_cpu_temperature() -> float:
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def get_temperature() -> int:
    global temps
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    temps = temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    return raw_temp - ((avg_cpu_temp - raw_temp) / factor)


def get_oxidising():
    data = gas.read_all()
    return data.oxidising / 1000


def get_reducing():
    data = gas.read_all()
    return data.reducing / 1000


def get_nh3():
    data = gas.read_all()
    return data.nh3 / 1000


def get_measurement() -> dict:
    global pms5003
    p_1 = 0
    p_2 = 0
    p_10 = 0

    try:
        pms_data = pms5003.read()
    except pmsReadTimeoutError as exception:
        logger.warning("Failed to read PMS5003 due to: {}".format(exception), exc_info=True)
        logger.info('Restarting sensor.. (it will takes ... 5 seconds')
        pms5003 = PMS5003()
        time.sleep(5)
    else:
        p_1 = float(pms_data.pm_ug_per_m3(1.0))
        p_2 = float(pms_data.pm_ug_per_m3(2.5))
        p_10 = float(pms_data.pm_ug_per_m3(10))

    measurement = {"temperature": get_temperature(),  # unit = "C"
                   "pressure": bme280.get_pressure(),  # unit = "hPa"
                   "humidity": bme280.get_humidity(),  # unit = "%"
                   "light": ltr559.get_lux(),  # unit = "Lux"
                   "proximity": ltr559.get_proximity(),
                   "oxidised": get_oxidising(),  # "oxidised"    unit = "kO"
                   "reduced": get_reducing(),  # unit = "kO"
                   "nh3": get_nh3(),  # unit = "kO"
                   "pm1": p_1,  # unit = "ug/m3"
                   "pm25": p_2,  # unit = "ug/m3"
                   "pm10": p_10}  # unit = "ug/m3"

    return measurement


# TODO remove it
def ui(msg: str, screen: bool = True):
    logger.info(msg)
    # print(msg)
    # FIXME temporary disabled
    '''
    if screen:
        denviro_display.draw_message(msg)
    '''


def setup():
    global temps
    global cpu_temps
    warm_up_measurement_counter = 10
    ui("Starting up... Warming up sensors")
    start_time = timer()
    cpu_temps = [get_cpu_temperature()] * warm_up_measurement_counter
    temps = [get_temperature()] * warm_up_measurement_counter
    end_time = timer()
    ui('It took {} ms.\nMounting drives...'.format(int((end_time - start_time) * 1000)))
    start_time = timer()
    commands.mount_all_drives('enviro')
    end_time = timer()
    ui('It took {} ms.'.format(int((end_time - start_time) * 1000)))


def main():
    measurement_counter = 0
    setup()
    while True:
        measurement_counter += 1
        ui('Measurement No.{}'.format(measurement_counter), False)

        start_time = timer()
        measurement = get_measurement()
        # FIXME temporary disabled  denviro_display.display_on_screen(measurement)
        measurement['cpu_temp'] = commands.get_cpu_temp()
        end_time = timer()
        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        measurement['measurement_time'] = measurement_time
        logger.info('it took ' + str(measurement_time) + ' milliseconds to measure it.')
        cl_display.print_measurement(measurement)
        # FIXME temporary disabled  denviro_display.set_brightness_for_screen(measurement['proximity'])
        data_files.store_enviro_measurement(measurement)
        # deprecated but i will change settings to send them via config settings
        # measurement_storage_service.send('enviro', measurement)
        sensor_warnings_service.get_current_warnings_for_enviro()
        remaining_time_in_millis = 5 - (float(measurement_time) / 1000)

        if remaining_time_in_millis > 0:
            time.sleep(remaining_time_in_millis)


if __name__ == '__main__':
    config_service.set_mode_to('enviro')
    data_files.setup_logging()
    ui('Starting application ... \n Press Ctrl+C to shutdown', True)
    ui('Logs config loaded.\nSending email', True)
    email_sender_service.send_ip_email('Denva Enviro+')
    ui('Email sent.\nRunning application', True)

    try:
        commands.mount_all_drives()
        main()
    except KeyboardInterrupt as keyboard_exception:
        logger.error('Something went badly wrong\n{}'.format(keyboard_exception), exc_info=True)
        # FIXME temporary disabled  denviro_display.draw_message('APP crashed.')
        sys.exit(0)
    # FIXME temporary disabled denviro_display.draw_message('Goodbye.')
