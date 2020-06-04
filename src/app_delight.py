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

import time
import unicornhathd

import config_service
from common import data_files, dom_utils, status
from delight import delight_display, delight_service, delight_utils
from gateways import local_data_gateway

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

        if clock % 500 == 0:
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
    unicornhathd.set_pixel(to_x(1), 9, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(1), 10, color_red, color_green, color_blue)
    logger.info('Dump daemon: {}'.format(state.get_status_as_light_colour()))

    state = status.Status()

    if 'digest' not in radar_data or radar_data["digest"] != 'UP':
        logger.warning('status: RED due to Data Digest is DOWN')
        state.set_error()

    color_red, color_green, color_blue = delight_utils.get_state_colour(state)
    unicornhathd.set_pixel(to_x(3), 9, color_red, color_green, color_blue)
    unicornhathd.set_pixel(to_x(3), 10, color_red, color_green, color_blue)
    logger.info('Data digest: {}'.format(state.get_status_as_light_colour()))

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


def startup():
    unicornhathd.brightness(0.9)
    for x in range(0, 16):
        for y in range(0, 16):
            unicornhathd.set_pixel(x, y, 255, 255, 255)
    unicornhathd.show()
    time.sleep(5)


def main():
    while True:
        if is_night_mode():
            device_status()
            local_data_gateway.post_healthcheck_beat('server', 'app')
        else:
            local_data_gateway.post_healthcheck_beat('server', 'app')
            device_status()
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('server', 'app')
            sub_light_travel()
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('server', 'app')
            in_the_warp()




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
        for coordinate_x in range(0, 16):
            for coordinate_y in range(0, 16):
                unicornhathd.set_pixel(coordinate_x, coordinate_y, 255, 0, 0)
        unicornhathd.show()
