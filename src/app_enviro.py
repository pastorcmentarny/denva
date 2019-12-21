#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import colorsys
import os
from timeit import default_timer as timer

import ST7735
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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import logging
import random
import cl_display
import commands
import data_files

logger = logging.getLogger('app')

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
pms5003 = PMS5003()

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=6,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height

# Set up canvas and font
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
path = os.path.dirname(os.path.realpath(__file__))
font = ImageFont.truetype(path + "/fonts/Roboto-Regular.ttf", 18)

message = ""

# The position of the top bar
top_pos = 25


# Displays data and text on the 0.96" LCD
def display_text(variable, data, unit):
    # Maintain length of list
    values[variable] = values[variable][1:] + [data]
    # Scale the values for the variable between 0 and 1
    colours = [(v - min(values[variable]) + 1) / (max(values[variable])
                                                  - min(values[variable]) + 1) for v in values[variable]]
    # Format the variable name and value
    message = "{}: {:.1f} {}".format(variable[:4], data, unit)
    logging.info(message)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (255, 255, 255))
    for i in range(len(colours)):
        # Convert the values to colours from red to blue
        colour = (1.0 - colours[i]) * 0.6
        r, g, b = [int(x * 255.0) for x in colorsys.hsv_to_rgb(colour,
                                                               1.0, 1.0)]
        # Draw a 1-pixel wide rectangle of colour
        draw.rectangle((i, top_pos, i+1, HEIGHT), (r, g, b))
        # Draw a line graph in black
        line_y = HEIGHT - (top_pos + (colours[i] * (HEIGHT - top_pos))) \
                 + top_pos
        draw.rectangle((i, line_y, i+1, line_y+1), (0, 0, 0))
    # Write the text at the top in black
    draw.text((0, 0), message, font=font, fill=(0, 0, 0))
    st7735.display(img)


# Get the temperature of the CPU for compensation
def get_cpu_temperature() -> float:
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 0.8



delay = 0.5  # Debounce the proximity tap
mode = 0     # The starting mode
last_page = 0
light = 1

# Create a values dict to store the data
variables = ["temperature",
             "pressure",
             "humidity",
             "light",
             "oxidised",
             "reduced",
             "nh3",
             "pm1",
             "pm25",
             "pm10"]

values = {}

for v in variables:
    values[v] = [1] * WIDTH

temps = []
cpu_temps = []


def get_temperature() ->int:
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
    p_1 = 0
    p_2 = 0
    p_10 = 0

    try:
        pms_data = pms5003.read()
    except pmsReadTimeoutError as e:
        logger.warning("Failed to read PMS5003 due to: {}".format(e), exc_info=True)
    else:
            p_1 = float(pms_data.pm_ug_per_m3(1.0))
            p_2 = float(pms_data.pm_ug_per_m3(2.5))
            p_10 = float(pms_data.pm_ug_per_m3(10))

    measurement = {"temperature" : get_temperature(), #unit = "C"
                   "pressure" : bme280.get_pressure(), #unit = "hPa"
                     "humidity" : bme280.get_humidity(),  #        unit = "%"
                     "light" : ltr559.get_lux(), #        unit = "Lux"
                   "proximity" : ltr559.get_proximity(),
                   "oxidised" : get_oxidising(),     #"oxidised"    unit = "kO"
                   "reduced" : get_reducing(), #unit = "kO"
                     "nh3" : get_nh3(), #unit = "kO"
                     "pm1" : p_1, #unit = "ug/m3"
                     "pm25" : p_2, #unit = "ug/m3"
                     "pm10" : p_10}  #unit = "ug/m3"

    return measurement


def setup():
    global temps
    global cpu_temps
    cpu_temps = [get_cpu_temperature()] * 5
    temps= [get_temperature()] * 5


def display_on_screen(measurement: dict):
    line2 = 'pm1: {} pm2.5: {} pm10: {}'.format(measurement["pm1"],measurement["pm25"],measurement["pm10"])
    line3 = 'nh3: {:.1f} '.format(measurement["nh3"])
    draw.text((0, 0), commands.get_ip(), font=font, fill=(random.randrange(0,255,1), random.randrange(0,255,1), random.randrange(0,255,1)))
    draw.text((0, 22), line2, font=font, fill=(random.randrange(0,255,1), random.randrange(0,255,1), random.randrange(0,255,1)))
    draw.text((0, 44), line3, font=font, fill=(random.randrange(0,255,1), random.randrange(0,255,1), random.randrange(0,255,1)))
    st7735.display(img)


def main():
    measurement_counter = 0
    setup()
    print(str(cpu_temps))
    while True:
        measurement_counter += 1
        logger.info('Getting measurement no.{}'.format(measurement_counter))

        start_time = timer()
        measurement = get_measurement()
        display_on_screen(measurement)
        end_time = timer()
        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        measurement['measurement_time'] = measurement_time
        logger.debug('it took ' + str(measurement_time) + ' microseconds to measure it.')
        cl_display.print_measurement(measurement)

        data_files.store_enviro_measurement(measurement)

        remaining_time_in_millis = 2 - (float(measurement_time) / 1000)

        if remaining_time_in_millis > 0:
            time.sleep(remaining_time_in_millis)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    data_files.setup_logging()
    logger.info('logs config loaded')
    try:
        main()
    except KeyboardInterrupt as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        sys.exit(0)
