#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

import config
from common import commands, get_description_for
import dom_utils
from gateways import web_data_gateway
from services import sensor_warnings_service
from services import system_data_service

logger = logging.getLogger('app')

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

cycle = 0


def display_information(message: str):
    img = Image.open("/home/ds/denva-master/src/images/background.png").convert(oled.mode)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (128, 128)], fill="black")
    draw.text((0, 0), message, fill="white", font=rr_12)
    oled.display(img)


def draw_image_on_screen(data, app_uptime):
    global cycle
    warnings_list = sensor_warnings_service.get_warnings_as_list(data)
    img = Image.open("/home/ds/denva-master/src/images/background.png").convert(oled.mode)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (128, 128)], fill="black")
    if len(warnings_list) > 0 and cycle % 3 == 2:
        draw.text((0, 0), "WARNINGS", fill="white", font=rr_14)
        y = 2
        for warning in warnings_list:
            y += 14
            draw.text((0, y), warning, fill="white", font=rr_12)
    elif cycle % 6 == 1:
        statuses = web_data_gateway.get_status()
        draw.text((0, 0), "Train & Tubes", fill="white", font=rr_14)
        y = 2
        for status in statuses:
            y += 14
            draw.text((0, y), status, fill="white", font=rr_12)
    else:
        draw.text((0, 0), f"Temp: {data[config.FIELD_TEMPERATURE]}", fill="white", font=rr_12)
        draw.text((0, 14), f"Pressure: {data[config.FIELD_PRESSURE]}", fill="white", font=rr_12)
        if cycle % 2 == 0:
            draw.text((0, 28), f"Humidity: {data[config.FIELD_HUMIDITY]}", fill="white", font=rr_12)
            draw.text((0, 42), f"Motion: {data['motion']:05.02f}", fill="white", font=rr_12)
            draw.text((0, 56), f"Colour: {dom_utils.get_color_name(data[config.FIELD_COLOUR])}", fill="white", font=rr_12)
            draw.text((0, 70), f"UVA: {get_description_for.uv(data['uva_index'])}", fill="white", font=rr_12)
        else:
            draw.text((0, 28), f"eco2: {data[config.FIELD_ECO2]}", fill="white", font=rr_12)
            draw.text((0, 42), f"Tvoc: {get_description_for.iqa_from_tvoc(data[config.FIELD_TVOC])['score']}",
                      fill="white",
                      font=rr_12)
            draw.text((0, 56),
                      f"Brightness: {get_description_for.brightness(data[config.FIELD_RED], data[config.FIELD_GREEN], data[config.FIELD_BLUE])}",
                      fill="white", font=rr_12)
            draw.text((0, 70), f"UVB: {get_description_for.uv(data['uvb_index'])}", fill="white", font=rr_12)

    if cycle % 7 == 0:
        draw.text((0, 84), f'CPU: {commands.get_cpu_temp()}', fill="white", font=rr_12)
    elif cycle % 7 == 1:
        draw.text((0, 84), commands.get_uptime(), fill="white", font=rr_12)
    elif cycle % 7 == 2:
        draw.text((0, 84), f'CPU: {commands.get_cpu_speed()}', fill="white", font=rr_12)
    elif cycle % 7 == 3:
        draw.text((0, 84), f'IP: {commands.get_ip()}', fill="white", font=rr_12)
    elif cycle % 7 == 4:
        draw.text((0, 84), f'Space: {commands.get_space_available()} MB', fill="white", font=rr_12)
    elif cycle % 7 == 6:
        draw.text((0, 84), f'RAM avail.: {system_data_service.get_memory_available_in_mb()}', fill="white",
                  font=rr_12)
    else:
        draw.text((0, 84), app_uptime, fill="white", font=rr_12)

    oled.display(img)
    cycle += 1
    if cycle > 12:
        cycle = 0
