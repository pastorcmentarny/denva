import json
import logging
import random
import re
import time
from datetime import datetime

import psutil
import requests

import config
import dom_utils
from common import commands
from server import display, sub_light, forest, warp
from server import healthcheck_service
from server import night_train_effect

logger = logging.getLogger('app')
dom_utils.setup_test_logging('display', False)

READ = 'r'
OFF = 'OFF'
ERROR = 'ERROR'
WARN = 'WARN'
CAUTION = 'CAUTION'
OK = 'OK'
PERFECT = 'PERFECT'
GOOD = 'GOOD'
POOR = 'POOR'
UNKNOWN = 'UNKNOWN'

DENVA_TWO = 'Denva TWO'


# TODO MERGE OK,UP,ON
def get_state_colour_for_hc(current_state: str):
    if current_state == OK:
        color_red = 0
        color_green = 255
        color_blue = 0
    elif current_state == ERROR:
        color_red = 255
        color_green = 0
        color_blue = 0
    elif current_state == WARN:
        color_red = 255
        color_green = 110
        color_blue = 0
    elif current_state == CAUTION:
        color_red = 255
        color_green = 224
        color_blue = 0
    elif current_state == OFF:
        color_red = 0
        color_green = 0
        color_blue = 127
    else:
        color_red = 64
        color_green = 64
        color_blue = 64
    return color_red, color_green, color_blue


# TODO move
def draw_cpu_status():
    temp = commands.get_cpu_temperature()
    if temp > 70.0:
        r, g, b = get_state_colour_for_hc(ERROR)
    elif temp > 60.0:
        r, g, b = get_state_colour_for_hc(WARN)
    elif temp > 50.0:
        r, g, b = get_state_colour_for_hc(CAUTION)
    else:
        r, g, b = get_state_colour_for_hc(OK)
    display.unicornhathd.set_pixel(1, 1, r, g, b)
    display.unicornhathd.set_pixel(1, 2, r, g, b)


# TODO move
def get_ram_available():
    return psutil.virtual_memory().available / 1000000


def draw_ram_status():
    ram = int(get_ram_available())
    if ram < 500:
        r, g, b = get_state_colour_for_hc(ERROR)
    elif ram < 1000:
        r, g, b = get_state_colour_for_hc(WARN)
    elif ram < 2000:
        r, g, b = get_state_colour_for_hc(CAUTION)
    else:
        r, g, b = get_state_colour_for_hc(OK)
    display.unicornhathd.set_pixel(1, 4, r, g, b)
    display.unicornhathd.set_pixel(1, 5, r, g, b)


# TODO re-use commands


def draw_storage_status():
    space = int(commands.get_space_available())
    if space < 250:
        r, g, b = get_state_colour_for_hc(ERROR)
    elif space < 512:
        r, g, b = get_state_colour_for_hc(WARN)
    elif space < 1000:
        r, g, b = get_state_colour_for_hc(CAUTION)
    else:
        r, g, b = get_state_colour_for_hc(OK)
    display.unicornhathd.set_pixel(1, 7, r, g, b)
    display.unicornhathd.set_pixel(1, 8, r, g, b)


# TODO move it to data_files
def load_network_health_check_results():
    try:
        with open("data/nhc.json", READ, encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as exception:
        return {
            "status": UNKNOWN,
            "result": "Unable to load file",
            "problems": [str(exception)]
        }


def draw_network_health_check():
    result = load_network_health_check_results()
    print(result)
    status = result['status']
    if status == PERFECT:
        r, g, b = get_state_colour_for_hc(OK)
    elif status == GOOD:
        r, g, b = get_state_colour_for_hc(CAUTION)
    elif status == POOR:
        r, g, b = get_state_colour_for_hc(WARN)
    elif status == OFF:
        r, g, b = get_state_colour_for_hc(ERROR)
    else:
        r, g, b = get_state_colour_for_hc(UNKNOWN)

    display.unicornhathd.set_pixel(1, 10, r, g, b)
    display.unicornhathd.set_pixel(1, 11, r, g, b)


def draw_denva2_status():
    # DEVICE
    status = healthcheck_service.get_device_status_for('denva2', 'device')
    if status == OFF:
        r, g, b = get_state_colour_for_hc(OFF)
        logger.info(f'{DENVA_TWO} is OFF')
        display.unicornhathd.set_pixel(11, 1, r, g, b)
        display.unicornhathd.set_pixel(11, 2, r, g, b)
        display.unicornhathd.set_pixel(11, 3, r, g, b)
        display.unicornhathd.set_pixel(11, 4, r, g, b)
        display.unicornhathd.set_pixel(11, 5, r, g, b)
        display.unicornhathd.set_pixel(11, 6, r, g, b)
        display.unicornhathd.set_pixel(11, 7, r, g, b)
        display.unicornhathd.set_pixel(11, 8, r, g, b)
    else:
        print(f'{DENVA_TWO} device status: {status}')
        logger.info(f'{DENVA_TWO} device status: {status}')
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 1, r, g, b)
        display.unicornhathd.set_pixel(11, 2, r, g, b)

        # UI
        status = healthcheck_service.is_up('denva2', 'ui')
        logger.info(f'{DENVA_TWO} UI status: ' + status)
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 4, r, g, b)

        # gps
        status = healthcheck_service.is_up('denva2', 'gps')
        logger.info(f'{DENVA_TWO} GPS status: ' + status)
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 6, r, g, b)

        # barometric
        status = healthcheck_service.is_up('denva2', 'barometric')
        logger.info(f'{DENVA_TWO} barometric status: ' + status)
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 7, r, g, b)

        # motion
        status = healthcheck_service.is_up('denva2', 'motion')
        logger.info(f'{DENVA_TWO} motion status: ' + status)
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 8, r, g, b)

        # spectrometer
        status = healthcheck_service.is_up('denva2', 'spectrometer')
        logger.info(f'{DENVA_TWO} spectrometer status: ' + status)
        r, g, b = get_state_colour_for_hc(status)
        display.unicornhathd.set_pixel(11, 9, r, g, b)


# DATA NEED BE SEND APP AND UI
def draw_denva_status():
    # DEVICE
    status = healthcheck_service.get_device_status_for('denva', 'device')
    print(f'denva device status: {status}')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(13, 1, r, g, b)
    display.unicornhathd.set_pixel(13, 2, r, g, b)

    # APP
    status = healthcheck_service.is_up('denva', 'app')
    print(f'denva app status: ' + status)
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(13, 4, r, g, b)
    display.unicornhathd.set_pixel(13, 5, r, g, b)

    # UI
    status = healthcheck_service.is_up('denva', 'ui')
    print(f'denva ui status: ' + status)
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(13, 7, r, g, b)
    display.unicornhathd.set_pixel(13, 8, r, g, b)


def draw_radar_status():
    status = healthcheck_service.is_up('knyszogar', 'radar')
    print(f'radar status: ' + status)
    r, g, b = get_state_colour_for_hc(status)
    # APPLICATION
    display.unicornhathd.set_pixel(12, 13, r, g, b)
    display.unicornhathd.set_pixel(12, 14, r, g, b)

    status = healthcheck_service.is_up('knyszogar', 'digest')
    print(f'digest app status: ' + status)
    r, g, b = get_state_colour_for_hc(status)
    # DIGEST
    display.unicornhathd.set_pixel(14, 13, r, g, b)
    display.unicornhathd.set_pixel(14, 14, r, g, b)


def get_data_for(url: str, timeout: int = 1) -> str:
    try:
        with requests.get(url, timeout=timeout) as response:
            response.raise_for_status()
            data_response = response.text
            return json.loads(data_response)["status"]
    except Exception as whoops:
        logger.error(f"Unable to get data from url: {url} due to {whoops}")
        return ERROR


def draw_knyszogar_app():
    status = healthcheck_service.is_up('knyszogar', 'app')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(3, 1, r, g, b)
    display.unicornhathd.set_pixel(3, 2, r, g, b)


def draw_knyszogar_email():
    status = healthcheck_service.is_up('knyszogar', 'email')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(3, 4, r, g, b)
    display.unicornhathd.set_pixel(3, 5, r, g, b)


def draw_knyszogar_hc():
    status = healthcheck_service.is_up('knyszogar', 'hc')
    print(f'HC status: {status}')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(3, 7, r, g, b)
    display.unicornhathd.set_pixel(3, 8, r, g, b)


def draw_knyszogar_www():
    status = healthcheck_service.is_up('server', 'ui')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(3, 10, r, g, b)
    display.unicornhathd.set_pixel(3, 11, r, g, b)


def draw_transport_manager_ui():
    hc_result = get_data_for(config.SERVER_IP + ":18001/actuator/health")
    r, g, b = get_state_colour_for_hc(hc_result)
    display.unicornhathd.set_pixel(3, 13, r, g, b)


def draw_transport_manager_service():
    hc_result = get_data_for(config.SERVER_IP + ":18002/actuator/health")
    r, g, b = get_state_colour_for_hc(hc_result)
    display.unicornhathd.set_pixel(3, 14, r, g, b)


def draw_transport_manager_db():
    hc_result = get_data_for(config.SERVER_IP + ":18003/actuator/health")
    r, g, b = get_state_colour_for_hc(hc_result)
    display.unicornhathd.set_pixel(3, 15, r, g, b)


def draw_camera_status():
    status = healthcheck_service.is_up('knyszogar', 'cctv')
    r, g, b = get_state_colour_for_hc(status)
    display.unicornhathd.set_pixel(10, 13, r, g, b)
    display.unicornhathd.set_pixel(10, 14, r, g, b)


def random_pixel():
    display.unicornhathd.set_pixel(0, 15, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    display.unicornhathd.set_pixel(0, 14, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    display.unicornhathd.set_pixel(1, 14, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    display.unicornhathd.set_pixel(1, 15, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


tick = True
# Change led location to next to random color
def draw_wifi_status():
    global tick
    wifi_status = commands.is_internet_up('192.168.0.200')
    if wifi_status:
        r, g, b = get_state_colour_for_hc('OK')
    else:
        r, g, b = get_state_colour_for_hc('ERROR')

    if tick:
        display.unicornhathd.set_pixel(8, 13, r, g, b)
        display.unicornhathd.set_pixel(8, 14, 24, 24, 24)
        tick = False
    else:
        display.unicornhathd.set_pixel(8, 13, 24, 24, 24)
        display.unicornhathd.set_pixel(8, 14, r, g, b)
        tick = True


def show_status():
    draw_cpu_status()
    draw_ram_status()
    draw_storage_status()
    draw_network_health_check()
    draw_denva_status()
    draw_denva2_status()
    draw_camera_status()
    draw_radar_status()
    draw_knyszogar_app()
    draw_knyszogar_email()
    draw_knyszogar_hc()
    draw_knyszogar_www()
    draw_transport_manager_ui()
    draw_transport_manager_service()
    draw_transport_manager_db()
    draw_wifi_status()
    random_pixel()
    display.unicornhathd.show()


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def run_random_animation():
    chance = random.randint(1, 4)
    if chance == 0:
        show_status()
    elif chance == 1:
        sub_light.sub_light_travel()
    elif chance == 2:
        forest.in_the_forest()
    elif chance == 3:
        warp.in_the_warp()
    elif chance == 4:
        night_train_effect.run_night_train()
    else:
        show_status()


def loop():
    while True:
        if is_night_mode():
            display.unicornhathd.brightness(0.1)
            display.reset_screen()
            show_status()
            time.sleep(10)
            chance = random.randint(1, 100)
            if chance > 30:
                display.reset_screen()
                for _ in range(1, random.randint(1, 3)):
                    run_random_animation()
                display.reset_screen()
        else:
            show_status()
            time.sleep(5)
            chance = random.randint(1, 100)
            if chance > 84:
                display.reset_screen()
                for _ in range(1, random.randint(1, 3)):
                    run_random_animation()
                display.reset_screen()


def startup():
    brightness_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    colour_list = [[185, 185, 185], [0, 0, 185], [128, 28, 200], [0, 185, 0], [255, 255, 255], [185, 0, 0],
                   [185, 153, 26], [185, 80, 0]]
    random.shuffle(colour_list)
    for count in range(0, 8):
        display.unicornhathd.brightness(brightness_list[count])
        display.set_all_pixel_to(colour_list[count][0], colour_list[count][1], colour_list[count][2])
        display.unicornhathd.show()
        time.sleep(0.5)
    display.reset_screen()
    display.unicornhathd.brightness(0.1)


if __name__ == '__main__':
    startup()
    loop()
