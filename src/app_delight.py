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
from datetime import datetime
from random import randint

import numpy  # try to get replace it
import time
import unicornhathd

import config_service
from common import data_files, dom_utils, status
from delight import delight_display, delight_service, delight_utils
from gateways import local_data_gateway
from systemhc import system_health_prototype

logger = logging.getLogger('app')

BLUE = 'blue'
GREY = 'grey'
GREEN = 'green'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
YELLOW = 'yellow'

unicornhathd.rotation(180)
DEFAULT_BRIGHTNESS_LEVEL = 0.3
unicornhathd.brightness(DEFAULT_BRIGHTNESS_LEVEL)

colors = [ORANGE, GREEN, GREY, BLUE, PURPLE, RED, YELLOW]  # change generate function too


def get_population() -> list:
    people = []
    for color in colors:
        people.append([randint(0, 15), 15, color])
    return people


blue_pilled_population = get_population()
clock = 0
cycle = 0

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
    global cycle
    cycle += 1
    logger.info('Spacedate: {}. Currently, we are in sub space zone..'.format(cycle))

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

        if clock % 125 == 0:
            running = False


def to_x(i: int) -> int:
    return 15 - i


def update_blink(blink, state) -> bool:
    if blink:
        return blink
    elif state != 2:
        logger.debug('Set animation to blinking')
        return True
    return False


def device_status():
    global cycle
    cycle += 1
    logger.info('Checking devices status... (Cycle: {})'.format(cycle))

    blink = False
    # 1. denva, 2. denviro, 3. server, 4. delight 5. radar
    unicornhathd.rotation(270)

    delight_display.reset_screen()
    cfg = config_service.load_cfg()
    purple_r = 160
    purple_g = 32
    purple_b = 240

    # 1. DENVA
    state = status.Status()
    logger.info('Getting status for denva..')
    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['denva']))

    if 'error' in server_data:
        logger.warning('Unable to get Denva status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_prototype.update_hc_for('denva', 'ui')
        if float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg['sensor']['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Denva )')
            state.set_error()
        elif float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg['sensor']['cpu_temp_warn']:
            logger.warning('status: ORANGE due to high cpu temp on Denva )')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 384:
            logger.warning('status: RED due to very low memory available on Denva')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Memory Available']) < 512:
            logger.warning('status: ORANGE due to low memory available on Denva')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Free Space']) < 256:
            logger.warning('status: RED due to very low free space on Denva')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Free Space']) < 1024:
            logger.warning('status: ORANGE due to low free space on Denva')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
            logger.warning('status: RED due to very low data free space on Denva')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
            logger.warning('status: ORANGE due to low data free space on Denva')
            state.set_warn()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    blink = update_blink(blink, state.state)
    unicornhathd.set_pixel(to_x(1), 1, purple_r, purple_g, purple_b)
    set_status_for_device(1, 13, color_red, color_green, color_blue)
    logger.info('Denva: {}'.format(state.get_status_as_light_colour()))

    # 2. DENVIRO
    state = status.Status()
    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['enviro']))

    if 'error' in server_data:
        logger.warning('Unable to get Denviro status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_prototype.update_hc_for('denviro', 'ui')
        if float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg['sensor']['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Denviro')
            state.set_error()
        elif float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg['sensor']['cpu_temp_warn']:
            logger.warning('status: ORANGE due to high cpu temp on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 384:
            logger.warning('status: RED due to very low memory available on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Memory Available']) < 512:
            logger.warning('status: ORANGE due to low memory available on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Free Space']) < 256:
            logger.warning('status: RED due to very low free space on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Free Space']) < 1024:
            logger.warning('status: ORANGE due to low free space on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
            logger.warning('status: RED due to very low data free space on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
            logger.warning('status: ORANGE due to low data free space on Denviro')
            state.set_warn()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    blink = update_blink(blink, state.state)

    unicornhathd.set_pixel(to_x(5), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(7), 1, purple_r, purple_g, purple_b)
    set_status_for_device(5, 13, color_red, color_green, color_blue)
    logger.info('Denviro: {}'.format(state.get_status_as_light_colour()))

    # 3. MOTHERSHIP SERVER
    state = status.Status()

    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['server']))

    if 'error' in server_data:
        logger.warning('Unable to get Server status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_prototype.update_hc_for('server', 'ui')
        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 384:
            logger.warning('status: RED due to very low memory available on Server')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Memory Available']) < 512:
            logger.warning('status: ORANGE due to low memory available on Server')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Disk Free']) < 256:
            logger.warning('status: RED due to very low disk free space on Server')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Disk Free']) < 1024:
            logger.warning('status: RED due to low disk free space on Server')
            state.set_warn()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    blink = update_blink(blink, state.state)

    unicornhathd.set_pixel(to_x(9), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(11), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(9), 3, purple_r, purple_g, purple_b)
    set_status_for_device(9, 13, color_red, color_green, color_blue)
    logger.info('Server: {}'.format(state.get_status_as_light_colour()))

    # 4. DELIGHT
    state = status.Status()
    try:
        delight_data = delight_service.get_system_info()

        if float(dom_utils.get_float_number_from_text(delight_data['CPU Temp'])) > cfg['sensor']['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Delight')
            state.set_error()
        elif float(dom_utils.get_float_number_from_text(delight_data['CPU Temp'])) > cfg['sensor']['cpu_temp_warn']:
            logger.warning('status: ORANGE due to high cpu temp on Delight')
            state.set_warn()
        if dom_utils.get_int_number_from_text(delight_data['Memory Available']) < 128:
            logger.warning('status: RED due to very low memory available on Delight')
            state.set_error()
        elif dom_utils.get_int_number_from_text(delight_data['Memory Available']) < 256:
            logger.warning('status: ORANGE due to low memory available on Delight')
            state.set_warn()

        if dom_utils.get_int_number_from_text(delight_data['Free Space']) < 128:
            logger.warning('status: RED due to very low free space on Delight')
            state.set_error()
        elif dom_utils.get_int_number_from_text(delight_data['Free Space']) < 512:
            logger.warning('status: ORANGE due to low free space on Delight')
            state.set_warn()
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        state.set_error()
    delight_ui_response = local_data_gateway.get_data_for('{}/hc'.format(config_service.load_cfg()["urls"]['delight']))
    if not 'error' in delight_ui_response:
        system_health_prototype.update_hc_for('delight', 'ui')

    color_blue, color_green, color_red = delight_utils.get_state_colour(state)
    blink = update_blink(blink, state.state)

    unicornhathd.set_pixel(to_x(13), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(15), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(13), 3, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(to_x(15), 3, purple_r, purple_g, purple_b)
    set_status_for_device(13, 13, color_red, color_green, color_blue)
    logger.info('Delight: {}'.format(state.get_status_as_light_colour()))

    # 5. DUMP (Aircraft Radar/ Digest)
    radar_data = delight_service.get_hc_for_radar()

    state = status.Status()

    if 'dump' not in radar_data or radar_data["dump"] != 'UP':
        logger.warning('status: RED due to Dump is DOWN')
        state.set_error()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    unicornhathd.set_pixel(to_x(2), 2, color_red, color_green, color_blue)
    logger.info('Dump daemon: {}'.format(state.get_status_as_light_colour()))

    state = status.Status()

    if 'digest' not in radar_data or radar_data["digest"] != 'UP':
        logger.warning('status: RED due to Data Digest is DOWN')
        state.set_error()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    unicornhathd.set_pixel(to_x(14), 2, color_red, color_green, color_blue)

    logger.info('Data digest: {}'.format(state.get_status_as_light_colour()))

    system_health_status = system_health_prototype.get_system_healthcheck()

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['denva']['app'])
    set_status_for_device(1, 7, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['denva']['ui'])
    set_status_for_device(1, 10, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['denviro']['app'])
    set_status_for_device(5, 7, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['denviro']['ui'])
    set_status_for_device(5, 10, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['server']['app'])
    set_status_for_device(9, 7, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['server']['ui'])
    set_status_for_device(9, 10, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['delight']['app'])
    set_status_for_device(13, 7, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['delight']['ui'])
    set_status_for_device(13, 10, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['other']['cctv'])
    unicornhathd.set_pixel(to_x(1), 4, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(2), 4, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(3), 4, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['other']['digest'])
    unicornhathd.set_pixel(to_x(13), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(14), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(15), 6, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['other']['radar'])
    unicornhathd.set_pixel(to_x(1), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(2), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(3), 6, color_red, color_green, color_blue)

    if is_night_mode():
        unicornhathd.brightness(0.1)
        unicornhathd.show()
        time.sleep(15)
    else:
        if blink:
            perform_state_animation()
        else:
            unicornhathd.brightness(DEFAULT_BRIGHTNESS_LEVEL)
            unicornhathd.show()
            time.sleep(30)

    unicornhathd.rotation(180)


def perform_state_animation():
    b1 = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19]
    b2 = [0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29]
    b3 = [0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39]
    b4 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49]
    b5 = [0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59]
    b6 = [0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69]
    brightnesses = [DEFAULT_BRIGHTNESS_LEVEL]
    brightnesses.extend(b3)
    brightnesses.extend(b4)
    brightnesses.extend(b5)
    brightnesses.extend(b6)
    b1.reverse()
    b2.reverse()
    b3.reverse()
    b4.reverse()
    b5.reverse()
    b6.reverse()
    brightnesses.extend(b6)
    brightnesses.extend(b5)
    brightnesses.extend(b4)
    brightnesses.extend(b3)
    brightnesses.extend(b2)
    brightnesses.extend(b1)
    b1.reverse()
    b2.reverse()
    b3.reverse()
    b4.reverse()
    b5.reverse()
    b6.reverse()
    brightnesses.extend(b1)
    brightnesses.extend(b2)
    for x in range(0, 15):
        for b in brightnesses:
            unicornhathd.brightness(b)
            unicornhathd.show()
            time.sleep(0.025)


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def set_status_for_device(x: int, y: int, color_red: int, color_green: int, color_blue: int):
    if is_night_mode():
        unicornhathd.set_pixel(to_x(delight_utils.get_random_pixel_location_at_night(x)), y + 2, color_red, color_green,
                               color_blue)
    else:
        unicornhathd.set_pixel(to_x(x), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(to_x(x + 1), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(to_x(x + 2), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(to_x(x), y + 2, color_red, color_green, color_blue)
        unicornhathd.set_pixel(to_x(x + 1), y + 2, color_red, color_green, color_blue)
        unicornhathd.set_pixel(to_x(x + 2), y + 2, color_red, color_green, color_blue)


def in_the_warp():
    global clock
    global cycle
    cycle += 1
    logger.info('Spacedate: {}. Currently, we are in the warp..'.format(cycle))

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


scale = 3

width, height = unicornhathd.get_shape()

forest_width = width * scale
forest_height = height * scale

hood_size = 3
avg_size = scale


def get_neighbours(x, y, z):
    return [(x2, y2) for x2 in range(x - (z - 1), x + z) for y2 in range(y - (z - 1), y + z) if (
            -1 < x < forest_width and -1 < y < forest_height and (x != x2 or y != y2) and (
            0 <= x2 < forest_width) and (0 <= y2 < forest_height))]


p = 0.01
f = 0.0005

tree = [0, 255, 0]
burning = [255, 0, 0]
space = [0, 0, 0]

trees = [[160, 32, 240], [0, 255, 0], [255, 255, 255]]
burning_colour = [[255, 0, 0], [255, 110, 0], [64, 64, 64]]


def initialise_forest():
    global tree
    global burning
    idx = random.randint(0, 2)
    tree = trees[idx]
    burning = burning_colour[idx]
    initial_trees = 0.55
    forest = [[tree if random.random() <= initial_trees else space for x in range(forest_width)] for y in
              range(forest_height)]
    return forest


def update_forest(forest):
    new_forest = [[space for x in range(forest_width)] for y in range(forest_height)]
    for x in range(forest_width):
        for y in range(forest_height):
            if forest[x][y] == burning:
                new_forest[x][y] = space
            #            elif forest[x][y] == space:
            #                new_forest[x][y] = tree if random.random() <= p else space
            elif forest[x][y] == tree:
                neighbours = get_neighbours(x, y, hood_size)
                new_forest[x][y] = (burning if any(
                    [forest[n[0]][n[1]] == burning for n in neighbours]) or random.random() <= f else tree)
    return new_forest


def average_forest(forest):
    avg_forest = [[space for x in range(width)] for y in range(height)]

    for i, x in enumerate(range(1, forest_width, scale)):
        for j, y in enumerate(range(1, forest_height, scale)):
            neighbours = get_neighbours(x, y, avg_size)
            red = int(numpy.mean([forest[n[0]][n[1]][0] for n in neighbours]))
            green = int(numpy.mean([forest[n[0]][n[1]][1] for n in neighbours]))
            blue = int(numpy.mean([forest[n[0]][n[1]][2] for n in neighbours]))
            avg_forest[i][j] = [red, green, blue]

    return avg_forest


def show_forest(forest):
    avg_forest = average_forest(forest)

    for x in range(width):
        for y in range(height):
            r, g, b = avg_forest[x][y]
            unicornhathd.set_pixel(x, y, int(r), int(g), int(b))

    unicornhathd.show()


def quit_if_burnt(forest):
    for x in range(forest_width):
        for y in range(forest_height):
            if forest[x][y] != space:
                return True  # it still burning
    return False


def in_the_forest():
    forest = initialise_forest()
    burnt = True
    while burnt:
        show_forest(forest)
        forest = update_forest(forest)
        burnt = quit_if_burnt(forest)


def startup():
    brightness_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    colour_list = [[185, 185, 185], [0, 0, 185], [128, 28, 200], [0, 185, 0], [255, 255, 255], [185, 0, 0],
                   [185, 153, 26], [185, 80, 0]]
    random.shuffle(colour_list)
    for count in range(0, 8):
        unicornhathd.brightness(brightness_list[count])
        set_all_pixel_to(colour_list[count][0], colour_list[count][1], colour_list[count][2])
        unicornhathd.show()
        time.sleep(0.5)


def main():
    startup()
    in_the_forest()
    while True:
        if is_night_mode():
            device_status()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
        else:
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            device_status()
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            sub_light_travel()
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            in_the_forest()
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            in_the_warp()


def set_all_pixel_to(red: int, green: int, blue: int):
    for coordinate_x in range(0, 16):
        for coordinate_y in range(0, 16):
            unicornhathd.set_pixel(coordinate_x, coordinate_y, red, green, blue)


if __name__ == '__main__':
    config_service.set_mode_to('delight')
    data_files.setup_logging('app')
    try:
        logger.info('Starting application ...')
        main()
    except KeyboardInterrupt as keyboard_exception:
        logger.error('Request to shutdown{}'.format(keyboard_exception), exc_info=True)
        unicornhathd.off()
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        unicornhathd.brightness(0.2)
        set_all_pixel_to(255, 0, 0)
        unicornhathd.show()
