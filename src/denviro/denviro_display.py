import config_service
import logging
import os
import random
import re

import ST7735
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import commands
from services import system_data_service

logger = logging.getLogger('app')

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
path = os.path.dirname(os.path.realpath(__file__))
WIDTH = st7735.width
HEIGHT = st7735.height
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(path + "/fonts/Roboto-Regular.ttf", 14)

def display_on_screen(measurement: dict):
    global cycle
    draw.rectangle((0, 0, 160, 80), fill="black")
    color1 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]
    color2 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]
    color3 = ['', random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)]
    line3 = ''

    if cycle % 6 == 0:
        line1 = 'CPU Temp: {}'.format(commands.get_cpu_temp())
        line2 = 'IP: {}'.format(commands.get_ip())
        line3 = 'Uptime: {}'.format(commands.get_uptime())
    elif cycle % 6 == 1:
        line1 = 'RAM avail.: {}'.format(system_data_service.get_memory_available_in_mb())
        line2 = 'Space: {}'.format(commands.get_space_available())
        line3 = 'Data Space: {}'.format(commands.get_data_space_available())

        color1 = get_colour_for_cpu()

    elif cycle % 6 == 2:
        line1 = 'light: {}'.format(measurement["light"])
        line2 = 'proximity: {}'.format(measurement["proximity"])
    elif cycle % 6 == 3:
        line1 = 'nh   3: {:.2f}'.format(measurement["nh3"])
        line2 = 'oxidised: {:.2f}'.format(measurement["oxidised"])
        line3 = 'reduced: {:.2f}'.format(measurement["reduced"])
    else:
        line1 = 'pm    1: {}'.format(measurement["pm1"])
        line2 = 'pm 2.5: {}'.format(measurement["pm25"])
        line3 = 'pm  10: {}'.format(measurement["pm10"])

        color1 = get_colour(measurement["pm1"])
        color2 = get_colour(measurement["pm25"])
        color3 = get_colour(measurement["pm10"])

    draw.text((0, 0), line1, font=font, fill=(color1[1], color1[2], color1[3]))
    draw.text((0, 16), line2, font=font, fill=(color2[1], color2[2], color2[3]))
    draw.text((0, 32), line3, font=font, fill=(color3[1], color3[2], color2[3]))
    #shade_of_grey = random.randrange(128, 255, 1)
    #draw.text((0, 48), line4, font=font, fill=(shade_of_grey, shade_of_grey, shade_of_grey))
    st7735.display(img)
    cycle += 1

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

def draw_message(msg: str):
    draw.rectangle((0, 0, 160, 80), fill="black")
    shade_of_grey = random.randrange(127, 255, 1)
    draw.text((0, 0), msg, font=font, fill=(shade_of_grey, shade_of_grey, shade_of_grey))
    st7735.display(img)


def get_colour_for_cpu():
    cpu_temp = float(re.sub('[^0-9.]', '', commands.get_cpu_temp()))
    config = config_service.load_cfg()
    if cpu_temp > config['sensor']['cpu_temp_fatal']:
        return ['Fatal', 255, 16, 1]
    elif cpu_temp > config['sensor']['cpu_temp_error']:
        return ['Fatal', 246, 108, 8]
    elif cpu_temp > config['sensor']['cpu_temp_warn']:
        return ['Warn', 255, 215, 0]
    else:
        return ['Good', 106, 168, 79]


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

