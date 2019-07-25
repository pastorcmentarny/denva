#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from luma.oled.device import sh1106
from luma.core.interface.serial import i2c

import commands
import get_description_for
import warning_utils

logger = logging.getLogger('app')


# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)


rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)


def draw_image_on_screen(data, cycle, app_uptime):
    warnings = warning_utils.get_warnings_as_list(data)
    for x in warnings:
        logging.info(x)
    img = Image.open("/home/pi/denva-master/src/images/background.png").convert(oled.mode)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (128, 128)], fill="black")
    if len(warnings) > 0 and cycle % 3 == 2:
        draw.text((0, 0), "WARNINGS", fill="white", font=rr_14)
        y = 2
        for warning in warnings:
            y += 14
            draw.text((0, y), warning, fill="white", font=rr_12)
    else:
        draw.text((0, 0), "Temp: {}".format(data["temp"]), fill="white", font=rr_12)
        draw.text((0, 14), "Pressure: {}".format(data["pressure"]), fill="white", font=rr_12)
        draw.text((0, 28), "Humidity: {}".format(data["humidity"]), fill="white", font=rr_12)
        draw.text((0, 42), "Motion: {:05.02f}".format(data["motion"]), fill="white", font=rr_12)
        if cycle % 2 == 0:
            draw.text((0, 56), "Colour: {}".format(data["colour"]), fill="white", font=rr_12)
            draw.text((0, 70), "UVA: {}".format(get_description_for.uv(data["uva_index"])), fill="white", font=rr_12)
        else:
            draw.text((0, 56), "Brightness: {}".format(get_description_for.brightness(data["r"], data["g"], data["b"])), fill="white", font=rr_12)
            draw.text((0, 70), "UVB: {}".format(get_description_for.uv(data["uvb_index"])), fill="white", font=rr_12)

    if cycle % 6 == 0:
        draw.text((0, 84), commands.get_cpu_temp(), fill="white", font=rr_12)
    elif cycle % 6 == 1:
        draw.text((0, 84), commands.get_uptime(), fill="white", font=rr_12)
    elif cycle % 6 == 2:
        draw.text((0, 84), commands.get_cpu_speed(), fill="white", font=rr_12)
    elif cycle % 6 == 3:
        draw.text((0, 84), commands.get_ip(), fill="white", font=rr_12)
    elif cycle % 6 == 4:
        draw.text((0, 84), 'Space: ' + commands.get_space_available() + 'MB', fill="white", font=rr_12)
    else:
        draw.text((0, 84), app_uptime, fill="white", font=rr_12)

    oled.display(img)
