#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz


app_delight
delight_ui web server,so you can run command from UI


idle animation
DESIGN:
def flight_between_planets():


"""
import logging
import random
from random import randint

import time
import unicornhathd

import config_service
import data_files
import local_data_gateway
import utils
from common import status
from delight import delight_display, delight_service

logger = logging.getLogger('app')

BLUE = 'blue'
GREY = 'grey'
GREEN = 'green'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
YELLOW = 'yellow'

unicornhathd.rotation(180)
unicornhathd.brightness(0.3)

colors = [ORANGE, GREEN, GREY, BLUE, PURPLE, RED, YELLOW]  # change generate function too


def get_population() -> list:
    people = []
    for color in colors:
        people.append([randint(0, 15), 15, color])
    return people


blue_pilled_population = get_population()
clock = 0

grey_rgb = [
    [154, 173, 154], [255, 255, 255], [235, 235, 235], [220, 220, 220],
    [185, 185, 185], [165, 165, 165], [128, 128, 128], [0, 0, 0]
]

blue_rgb = [
    [154, 173, 154], [0, 0, 255], [0, 0, 235], [0, 0, 220],
    [0, 0, 185], [0, 0, 165], [0, 0, 128], [0, 0, 0]
]

purple_rgb = [
    [154, 173, 154], [160, 32, 240], [144, 30, 220], [128, 28, 200],
    [112, 26, 180], [96, 24, 160], [80, 16, 120], [0, 0, 0]
]

green_rgb = [
    [154, 173, 154], [0, 255, 0], [0, 235, 0], [0, 220, 0],
    [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0]
]

red_rgb = [
    [154, 173, 154], [255, 0, 0], [235, 0, 0], [220, 0, 0],
    [185, 0, 0], [165, 0, 0], [128, 0, 0], [0, 0, 0]
]

yellow_rgb = [
    [154, 173, 154], [255, 224, 32], [235, 202, 30], [220, 188, 28],
    [185, 153, 26], [165, 133, 24], [128, 96, 22], [0, 0, 0]
]

orange_rgb = [
    [154, 173, 154], [255, 110, 0], [235, 101, 0], [220, 94, 0],
    [185, 80, 0], [165, 70, 0], [128, 55, 0], [0, 0, 0]
]


def generate_person_of_color(person_color: str, person: list):
    if person_color is ORANGE:
        shape = orange_rgb
    elif person_color is GREEN:
        shape = green_rgb
    elif person_color is GREY:
        shape = grey_rgb
    elif person_color is BLUE:
        shape = blue_rgb
    elif person_color is PURPLE:
        shape = purple_rgb
    elif person_color is RED:
        shape = red_rgb
    elif person_color is YELLOW:
        shape = yellow_rgb
    else:
        shape = []

    y = person[1]
    for rgb in shape:
        if (y < 15) and (y > 0):
            unicornhathd.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
        y += 1


def get_random_color() -> str:
    result = randint(0, len(colors) - 1)
    return colors[result]


def show_on_screen(pixel_list: list):
    delight_display.reset_screen()
    for element in pixel_list:
        unicornhathd.set_pixel(element[0], element[1], 235, 202, 30)
    unicornhathd.show()
    time.sleep(2.5)


def sub_light_travel():
    global clock

    logger.info('Spacedate: {}. Currently, we are in sub space zone..'.format(clock))

    running = True
    while running:
        for person in blue_pilled_population:
            person_color = person[2]
            generate_person_of_color(person_color, person)
            person[1] -= 1
        unicornhathd.set_pixel(0, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(15, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(0, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(15, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.show()
        time.sleep(0.075)
        clock += 1

        if clock % 5 == 0:
            blue_pilled_population.append([randint(0, 15), 15, get_random_color()])
        if clock % 7 == 0:
            blue_pilled_population.append([randint(0, 15), 15, get_random_color()])

        while len(blue_pilled_population) > 100:
            blue_pilled_population.pop(0)

        if clock % 1000 == 0:
            running = False


def to_x(i: int) -> int:
    return 15 - i


# TODO prorotype
def device_status():
    unicornhathd.rotation(90)

    delight_display.reset_screen()
    cfg = config_service.load_cfg()
    purple_r = 160
    purple_g = 32
    purple_b = 240

    state = status.Status()

    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['denva']))

    if utils.get_int_number_from_text(server_data['CPU Temp']) > cfg['sensor']['cpu_temp_error']:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['CPU Temp']) > cfg['sensor']['cpu_temp_warn']:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Memory Available']) < 384:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Memory Available']) < 512:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Free Space']) < 256:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Free Space']) < 1024:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
        state.set_warn()

    if state.get_status_as_light_colour() == state.ERROR:
        color_red = 255
        color_green = 0
        color_blue = 0
    elif state.get_status_as_light_colour() == state.WARN:
        color_red = 255
        color_green = 224
        color_blue = 32
    else:
        color_red = 0
        color_green = 255
        color_blue = 0

    unicornhathd.set_pixel(to_x(1), 1, purple_r, purple_g, purple_b)
    set_status_for_device(1, 1, color_red, color_green, color_blue)

    state = status.Status()

    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['enviro']))

    if utils.get_int_number_from_text(server_data['CPU Temp']) > cfg['sensor']['cpu_temp_error']:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['CPU Temp']) > cfg['sensor']['cpu_temp_warn']:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Memory Available']) < 384:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Memory Available']) < 512:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Free Space']) < 256:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Free Space']) < 1024:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
        state.set_warn()

    if state.get_status_as_light_colour() == state.ERROR:
        color_red = 255
        color_green = 0
        color_blue = 0
    elif state.get_status_as_light_colour() == state.WARN:
        color_red = 255
        color_green = 224
        color_blue = 32
    else:
        color_red = 0
        color_green = 255
        color_blue = 0

    unicornhathd.set_pixel(to_x(5), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(7), 1, purple_r, purple_g, purple_b)
    set_status_for_device(5, 13, color_red, color_green, color_blue)

    state = status.Status()

    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['server']))

    if utils.get_int_number_from_text(server_data['Memory Available']) < 384:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Memory Available']) < 512:
        state.set_warn()

    if utils.get_int_number_from_text(server_data['Disk Free']) < 256:
        state.set_error()
    elif utils.get_int_number_from_text(server_data['Disk Free']) < 1024:
        state.set_warn()

    if state.get_status_as_light_colour() == state.ERROR:
        color_red = 255
        color_green = 0
        color_blue = 0
    elif state.get_status_as_light_colour() == state.WARN:
        color_red = 255
        color_green = 224
        color_blue = 32
    else:
        color_red = 0
        color_green = 255
        color_blue = 0

    unicornhathd.set_pixel(to_x(9), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(11), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(9), 3, purple_r, purple_g, purple_b)
    set_status_for_device(9, 13, color_red, color_green, color_blue)

    state = status.Status()
    system_data = delight_service.get_system_info()

    if utils.get_int_number_from_text(system_data['Memory Available']) < 128:
        state.set_error()
    elif utils.get_int_number_from_text(system_data['Memory Available']) < 256:
        state.set_warn()

    if utils.get_int_number_from_text(system_data['Free Space']) < 128:
        state.set_error()
    elif utils.get_int_number_from_text(system_data['Free Space']) < 512:
        state.set_warn()

    if state.get_status_as_light_colour() == state.ERROR:
        color_red = 255
        color_green = 0
        color_blue = 0
    elif state.get_status_as_light_colour() == state.WARN:
        color_red = 255
        color_green = 224
        color_blue = 32
    else:
        color_red = 0
        color_green = 255
        color_blue = 0

    unicornhathd.set_pixel(to_x(13), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(15), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(13), 3, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(15), 3, purple_r, purple_g, purple_b)
    set_status_for_device(13, 13, color_red, color_green, color_blue)

    unicornhathd.show()
    brightnesses = [0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3]
    for x in range(0, 3):
        for b in brightnesses:
            unicornhathd.brightness(b)
            time.sleep(1)

    unicornhathd.rotation(180)


def set_status_for_device(x: int, y: int, color_red: int, color_green: int, color_blue: int):
    unicornhathd.set_pixel(to_x(x), y, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 1), y, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 2), y, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x), y + 1, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 1), y + 1, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 2), y + 1, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x), y + 2, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 1), y + 2, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(x + 2), y + 2, color_red, color_green, color_blue)


def in_the_warp():
    global clock

    logger.info('Spacedate: {}. Currently, we are in the warp..'.format(clock))

    star_count = 25
    star_speed = 0.01
    stars = []

    for i in range(0, star_count):
        stars.append((random.uniform(4, 11), random.uniform(4, 11), 0))

    running = True
    while running:
        unicornhathd.clear()
        clock += 1
        for i in range(0, star_count):
            stars[i] = (
                stars[i][0] + ((stars[i][0] - 8.1) * star_speed),
                stars[i][1] + ((stars[i][1] - 8.1) * star_speed),
                stars[i][2] + star_speed * 50)

            if stars[i][0] < 0 or stars[i][1] < 0 or stars[i][0] > 16 or stars[i][1] > 16:
                stars[i] = (random.uniform(4, 11), random.uniform(4, 11), 0)

            v = stars[i][2]

            unicornhathd.set_pixel(stars[i][0], stars[i][1], v, v, v)

        unicornhathd.show()

        if clock % 25 == 0:
            star_speed += 0.001
        if clock % 2000 == 0:
            running = False


def main():
    try:
        while True:
            device_status()
            delight_display.reset_screen()
            sub_light_travel()
            delight_display.reset_screen()
            in_the_warp()
    except KeyboardInterrupt:
        unicornhathd.off()


if __name__ == '__main__':
    config_service.set_mode_to('delight')
    data_files.setup_logging()
    main()
