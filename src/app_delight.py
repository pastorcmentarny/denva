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
import random
import time
import traceback
from datetime import datetime

import unicornhathd

import config
from common import data_files, status
import dom_utils
from delight import delight_display, delight_service, delight_utils, ui_utils, forest, sub_light, warp
from gateways import local_data_gateway
from systemhc import system_health_check_service

logger = logging.getLogger('app')

unicornhathd.rotation(180)

unicornhathd.brightness(config_service.get_default_brightness_for_delight_display())

clock = 0
cycle = 0

blink = False
purple_r = 160
purple_g = 32
purple_b = 240


def show_on_screen(pixel_list: list):
    delight_display.reset_screen()
    for element in pixel_list:
        unicornhathd.set_pixel(element[0], element[1], 235, 202, 30)
    unicornhathd.show()
    time.sleep(2.5)


def update_blink(state) -> bool:
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

    # 1. denva, 2. denviro, 3. server, 4. delight 5. radar
    unicornhathd.rotation(270)

    delight_display.reset_screen()
    cfg = config_service.load_cfg()

    set_denva_status(cfg)
    set_denviro_status(cfg)
    set_mothership_status()
    set_delight_status(cfg)

    system_health_status = system_health_check_service.get_system_healthcheck()

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
    unicornhathd.set_pixel(ui_utils.to_x(1), 4, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(2), 4, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(3), 4, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['other']['digest'])
    unicornhathd.set_pixel(ui_utils.to_x(13), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(14), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(15), 6, color_red, color_green, color_blue)

    color_red, color_green, color_blue = delight_utils.get_state_colour_for_hc(system_health_status['other']['radar'])
    unicornhathd.set_pixel(ui_utils.to_x(1), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(2), 6, color_red, color_green, color_blue)
    unicornhathd.set_pixel(ui_utils.to_x(3), 6, color_red, color_green, color_blue)

    if is_night_mode():
        unicornhathd.brightness(0.1)
        unicornhathd.show()
        time.sleep(15)
    else:
        if blink:
            ui_utils.perform_blink_animation(unicornhathd)
        else:
            unicornhathd.brightness(config_service.get_default_brightness_for_delight_display())
            unicornhathd.show()
            time.sleep(30)

    unicornhathd.rotation(180)


def set_delight_status(cfg):
    # 4. DELIGHT
    state = status.Status()
    try:
        delight_data = delight_service.get_system_info()

        cpu_temp = str(delight_data['CPU Temp'])
        if float(dom_utils.get_float_number_from_text(cpu_temp)) > cfg['sensor']['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Delight')
            state.set_error()
        elif float(dom_utils.get_float_number_from_text(cpu_temp)) > cfg['sensor']['cpu_temp_warn']:
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
    except Exception as set_state_exception:
        logger.error('Something went badly wrong\n{}'.format(set_state_exception), exc_info=True)
        state.set_error()
    delight_ui_response = local_data_gateway.get_data_for('{}/hc'.format(config_service.load_cfg()["urls"]['delight']))
    if not 'error' in delight_ui_response:
        system_health_check_service.update_hc_for('delight', 'ui')
    color_blue, color_green, color_red = delight_utils.get_state_colour(state)
    update_blink(state.state)
    unicornhathd.set_pixel(ui_utils.to_x(13), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(15), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(13), 2, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(15), 2, purple_r, purple_g, purple_b)
    set_status_for_device(13, 13, color_red, color_green, color_blue)
    logger.info('Delight: {}'.format(state.get_status_as_light_colour()))


def set_mothership_status():
    # 3. MOTHERSHIP SERVER
    state = status.Status()
    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['server']))
    if 'error' in server_data:
        logger.warning('Unable to get Server status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_check_service.update_hc_for('server', 'ui')
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
    update_blink(state.state)
    unicornhathd.set_pixel(ui_utils.to_x(9), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(11), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(9), 2, purple_r, purple_g, purple_b)
    set_status_for_device(9, 13, color_red, color_green, color_blue)
    logger.info('Server: {}'.format(state.get_status_as_light_colour()))


def set_denviro_status(cfg):
    # 2. DENVIRO
    state = status.Status()
    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['enviro']))
    if 'error' in server_data:
        logger.warning('Unable to get Denviro status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_check_service.update_hc_for('denviro', 'ui')
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
    update_blink(state.state)
    unicornhathd.set_pixel(ui_utils.to_x(5), 1, purple_r, purple_g, purple_b)
    unicornhathd.set_pixel(ui_utils.to_x(7), 1, purple_r, purple_g, purple_b)
    set_status_for_device(5, 13, color_red, color_green, color_blue)
    logger.info('Denviro: {}'.format(state.get_status_as_light_colour()))
    return blink


def set_denva_status(cfg):
    # 1. DENVA
    state = status.Status()
    logger.info('Getting status for denva..')
    server_data = local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['denva']))
    if 'error' in server_data:
        logger.warning('Unable to get Denva status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_check_service.update_hc_for('denva', 'ui')
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
    update_blink(state.state)
    unicornhathd.set_pixel(ui_utils.to_x(1), 1, purple_r, purple_g, purple_b)
    set_status_for_device(1, 13, color_red, color_green, color_blue)
    logger.info('Denva: {}'.format(state.get_status_as_light_colour()))
    return blink


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def set_status_for_device(x: int, y: int, color_red: int, color_green: int, color_blue: int):
    if is_night_mode():
        unicornhathd.set_pixel(ui_utils.to_x(delight_utils.get_random_pixel_location_at_night(x)), y + 2, color_red,
                               color_green,
                               color_blue)
    else:
        unicornhathd.set_pixel(ui_utils.to_x(x), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(ui_utils.to_x(x + 1), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(ui_utils.to_x(x + 2), y + 1, color_red, color_green, color_blue)
        unicornhathd.set_pixel(ui_utils.to_x(x), y + 2, color_red, color_green, color_blue)
        unicornhathd.set_pixel(ui_utils.to_x(x + 1), y + 2, color_red, color_green, color_blue)
        unicornhathd.set_pixel(ui_utils.to_x(x + 2), y + 2, color_red, color_green, color_blue)


def startup():
    brightness_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    colour_list = [[185, 185, 185], [0, 0, 185], [128, 28, 200], [0, 185, 0], [255, 255, 255], [185, 0, 0],
                   [185, 153, 26], [185, 80, 0]]
    random.shuffle(colour_list)
    for count in range(0, 8):
        unicornhathd.brightness(brightness_list[count])
        ui_utils.set_all_pixel_to(colour_list[count][0], colour_list[count][1], colour_list[count][2], unicornhathd)
        unicornhathd.show()
        time.sleep(0.5)


def main():
    startup()
    forest.in_the_forest(unicornhathd)
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
            sub_light.sub_light_travel(unicornhathd, clock, cycle)
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            device_status()
            delight_display.reset_screen()
            forest.in_the_forest(unicornhathd)
            delight_display.reset_screen()
            local_data_gateway.post_healthcheck_beat('delight', 'app')
            warp.in_the_warp(unicornhathd, clock, cycle)


if __name__ == '__main__':
    config_service.set_mode_to('delight')
    data_files.setup_logging('app')
    try:
        logger.info('Starting application ...')
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        unicornhathd.off()
    except Exception as exception:
        logger.error('Something went wrong\n{}'.format(exception), exc_info=True)
        unicornhathd.brightness(0.2)
        ui_utils.set_all_pixel_to(255, 0, 0, unicornhathd)
        unicornhathd.show()
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        logger.error(msg, exc_info=True)
        traceback.print_exc()
        unicornhathd.off()
