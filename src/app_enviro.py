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

import os
from timeit import default_timer as timer

import ST7735
import sys
import time

import config_serivce
import measurement_storage_service

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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import logging
import random
import cl_display
import commands
import data_files
import email_sender_service

logger = logging.getLogger('app')

bme280 = BME280()
pms5003 = PMS5003()
st7735 = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)
st7735.begin()

# setup
WIDTH = st7735.width
HEIGHT = st7735.height
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
path = os.path.dirname(os.path.realpath(__file__))
font = ImageFont.truetype(path + "/fonts/Roboto-Regular.ttf", 14)
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


def ui(msg: str, screen: bool = True):
    logger.info(msg)
    print(msg)
    if screen:
        draw_message(msg)


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


def display_on_screen(measurement: dict):
    global cycle
    draw.rectangle((0, 0, 160, 80), fill="black")
    color1 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]
    color2 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]
    color3 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]

    if cycle % 6 == 0:
        line1 = 'IP: {}'.format(commands.get_ip())
        line2 = 'CPU Temp: {}'.format(commands.get_cpu_temp())
        line3 = 'Uptime: {}'.format(commands.get_uptime())
        line4 = 'Space: {}'.format(commands.get_space_available())
    elif cycle % 6 == 1:
        line1 = 'light: {}'.format(measurement["light"])
        line2 = 'proximity: {}'.format(measurement["proximity"])
        line3 = 'oxidised: {:.2f}'.format(measurement["oxidised"])
        line4 = 'reduced: {:.2f}'.format(measurement["reduced"])
    else:
        line1 = 'pm   1: {}'.format(measurement["pm1"])
        line2 = 'pm 2.5: {}'.format(measurement["pm25"])
        line3 = 'pm  10: {}'.format(measurement["pm10"])
        line4 = 'nh   3: {:.2f}'.format(measurement["nh3"])
        color1 = get_colour(measurement["pm1"])
        color2 = get_colour(measurement["pm25"])
        color3 = get_colour(measurement["pm10"])
    draw.text((0, 0), line1, font=font, fill=(color1[1], color1[2], color1[3]))
    draw.text((0, 16), line2, font=font, fill=(color2[1], color2[2], color2[3]))
    draw.text((0, 32), line3, font=font, fill=(color3[1], color3[2], color2[3]))
    shade_of_grey = random.randrange(128, 255, 1)
    draw.text((0, 48), line4, font=font, fill=(shade_of_grey, shade_of_grey, shade_of_grey))
    st7735.display(img)
    cycle += 1


def get_colour(level: float) -> list:
    if level < 15.5:
        return ['Good', 0, 204, 0]
    elif level < 40.5:
        return ['Moderate', 255, 234, 0]
    elif level < 65.5:
        return ['Unhealthy for Sensitive', 255, 165, 0]
    elif level < 150.5:
        return ['Unhealthy', 255, 37, 0]
    elif level < 250.5:
        return ['Very Unhealthy', 165, 0, 255]
    elif level < 500.5:
        return ['Hazardous', 116, 0, 179]
    else:
        return ['Deadly?', 30, 30, 30]


def draw_message(msg: str):
    draw.rectangle((0, 0, 160, 80), fill="black")
    shade_of_grey = random.randrange(127, 255, 1)
    draw.text((0, 0), msg, font=font, fill=(shade_of_grey, shade_of_grey, shade_of_grey))
    st7735.display(img)

on = True

def set_brightness_for_screen(proximity):
    global on
    if proximity > 1000:
        on = not on
        if on:
            logger.info('switching ON backlight')
            st7735.set_backlight(12)
        else:
            logger.info('switching OFF backlight')
            st7735.set_backlight(0)


def main():
    measurement_counter = 0
    setup()
    while True:
        measurement_counter += 1
        ui('Measurement No.{}'.format(measurement_counter), False)

        start_time = timer()
        measurement = get_measurement()
        display_on_screen(measurement)
        end_time = timer()
        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        measurement['measurement_time'] = measurement_time
        logger.info('it took ' + str(measurement_time) + ' milliseconds to measure it.')
        cl_display.print_measurement(measurement)
        set_brightness_for_screen(measurement['proximity'])
        data_files.store_enviro_measurement(measurement)
        measurement_storage_service.send('enviro',measurement)
        remaining_time_in_millis = 2 - (float(measurement_time) / 1000)

        if remaining_time_in_millis > 0:
            time.sleep(remaining_time_in_millis)


if __name__ == '__main__':
    config_serivce.set_mode_to('enviro')
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
        draw_message('APP crashed.')
        sys.exit(0)
    draw_message('Goodbye.')

