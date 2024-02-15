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
from pathlib import Path
import dom_utils
from common import data_files

KEY_SYSTEM = "system"
KEY_LATENCY = "latency"
KEY_LOGS = "logs"
KEY_SENSORS = "sensors"
KEY_URLS = "urls"
KEY_OPTIONS = 'options'
KEY_PATH = "paths"

logger = logging.getLogger('app')

CPU_TEMP_FATAL = "cpu_temp_fatal"
CPU_TEMP_ERROR = "cpu_temp_error"
CPU_TEMP_WARN = "cpu_temp_warn"
MEASUREMENT_LIST_SIZE = 'measurement_list_size'

DENVA_DATA_COLUMN_TIMESTAMP = 0
DENVA_DATA_COLUMN_MEASUREMENT_TIME = 1
DENVA_DATA_COLUMN_TEMP = 2
DENVA_DATA_COLUMN_PRESSURE = 3
DENVA_DATA_COLUMN_HUMIDITY = 4
DENVA_DATA_COLUMN_GAS_RESISTANCE = 5
DENVA_DATA_COLUMN_COLOUR = 6
DENVA_DATA_COLUMN_R = 7
DENVA_DATA_COLUMN_G = 8
DENVA_DATA_COLUMN_B = 9
DENVA_DATA_COLUMN_CO2 = 10
DENVA_DATA_COLUMN_CO2_TEMPERATURE = 11
DENVA_DATA_COLUMN_RELATIVE_HUMIDITY = 12
DENVA_DATA_COLUMN_CPU_TEMP = 13
DENVA_DATA_COLUMN_ECO2 = 14
DENVA_DATA_COLUMN_TVOC = 15
DENVA_DATA_COLUMN_GPS_LATITUDE = 16
DENVA_DATA_COLUMN_GPS_LONGITUDE = 17
DENVA_DATA_COLUMN_GPS_ALTITUDE = 18
DENVA_DATA_COLUMN_GPS_LAT_DIR = 19
DENVA_DATA_COLUMN_GPS_LON_DIR = 20
DENVA_DATA_COLUMN_GPS_GEO_SEP = 21
DENVA_DATA_COLUMN_GPS_NUM_SATS = 22
DENVA_DATA_COLUMN_GPS_QUAL = 23
DENVA_DATA_COLUMN_GPS_SPEED_OVER_GROUND = 24
DENVA_DATA_COLUMN_GPS_MODE_FIX_TYPE = 25
DENVA_DATA_COLUMN_GPS_PDOP = 26
DENVA_DATA_COLUMN_GPS_HDOP = 27
DENVA_DATA_COLUMN_GPS_VDOP = 28

DEVICE_ON = 'OK'
DEVICE_OFF = 'OFF'

FIELD_CPU_TEMP = 'cpu_temp'
FIELD_RELATIVE_HUMIDITY = "relative_humidity"
FIELD_GPS_VDOP = 'vdop'
FIELD_GPS_HDOP = 'hdop'
FIELD_GPS_PDOP = 'pdop'
FIELD_GPS_MODE_FIX_TYPE = 'mode_fix_type'
FIELD_GPS_SPEED_OVER_GROUND = 'speed_over_ground'
FIELD_GPS_QUAL = 'gps_qual'
FIELD_GPS_NUM_SATS = 'num_sats'
FIELD_GPS_GEO_SEP = 'geo_sep'
FIELD_GPS_LON_DIR = 'lon_dir'
FIELD_GPS_LAT_DIR = 'lat_dir'
FIELD_GPS_ALTITUDE = 'altitude'
FIELD_GPS_LONGITUDE = 'longitude'
FIELD_MEASUREMENT_TIME = 'measurement_time'
FIELD_MEASUREMENT_COUNTER = 'measurement_counter'
FIELD_GPS_LATITUDE = 'latitude'
FIELD_BLUE = "b"
FIELD_GREEN = "g"
FIELD_RED = "r"
FIELD_COLOUR = "colour"
FIELD_ECO2 = "eco2"
FIELD_TVOC = "tvoc"
FIELD_GAS_RESISTANCE = 'gas_resistance'
FIELD_HUMIDITY = "humidity"
FIELD_PRESSURE = "pressure"
FIELD_TEMPERATURE = "temperature"
FIELD_TIMESTAMP = 'timestamp'
FIELD_CO2 = "co2"
FIELD_CO2_TEMPERATURE = "co2_temperature"
FIELD_LIGHT = 'light'
FIELD_PROXIMITY = 'proximity'
FIELD_OXIDISED = 'oxidised'
FIELD_REDUCED = 'reduced'
FIELD_NH3 = 'nh3'
FIELD_PM1 = 'p_1'
FIELD_PM25 = 'p_2'
FIELD_PM10 = 'p_10'
FIELD_SPECTROMETER_RED = 'spectometer_red'
FIELD_SPECTROMETER_ORANGE = 'orange'
FIELD_SPECTROMETER_YELLOW = 'yellow'
FIELD_SPECTROMETER_GREEN = 'green'
FIELD_SPECTROMETER_BLUE = 'blue'
FIELD_SPECTROMETER_VIOLET = 'violet'
FIELD_UVA = 'uva'
FIELD_UVB = 'uvb'
FIELD_UV = 'uv_index'

KEY_DENVA_TWO = 'denva2'

SERVER_IP = 'http://192.168.0.200'
DENVA_IP = 'http://192.168.0.201'
DENVA_TWO_IP = 'http://192.168.0.205'

REFRESH_RATE = 'refresh-rate'

PI_HOME_DIR = '/home/ds/'
PI_PROJECT_PATH = f'{PI_HOME_DIR}app'
PI_CONFIG_PATH = f'{PI_HOME_DIR}configs/'
PI_DATA_PATH = f'{PI_HOME_DIR}data/'
PI_LOGS_PATH = f'{PI_HOME_DIR}logs/'
PI_SENSORS_DATA_PATH = PI_DATA_PATH
PI_KNYSZOGAR_DATA = f'{PI_HOME_DIR}knyszogar/data/'
settings = {
    "mode": 'dev',
    KEY_SENSORS: {
        "cameras": {
            "cctv": False,
            "sky": False
        },
        "motion": {
            "shaking": 1000,
            "sensitivity": 8,
            "noOfFlashes": 5
        },
        "bme": {
            "warm_up": 10
        },
        "unicornhd": {
            "default_brightness": 0.3
        },
        "radar": True
    },
    KEY_PATH: {
        "frame": f'{PI_HOME_DIR}/frame/',
        "backup": f'{PI_HOME_DIR}backup/',
        "events": f'{PI_HOME_DIR}events.json',
        "chinese-dictionary": f'{PI_DATA_PATH}dictionary.txt',
        "overseer_mode": f'{PI_HOME_DIR}overseer_mode.txt',
        "text": f'{PI_DATA_PATH}text_to_display.txt',
        "healthcheck": f'/home/pi/data/hc.json',  # TODO update when user is moved to ds
        "all_warnings": f"{PI_DATA_PATH}all-warnings.txt"
    },
    REFRESH_RATE: {
        "fast": 0.25,
        "normal": 1,
        "slow": 5,
    },
    KEY_SYSTEM: {
        "memory_available": 250 * 1024 * 1024,  # 250MB
        "free_space": 500,
        "ip": f"{SERVER_IP}:5000",
        CPU_TEMP_WARN: 60,
        CPU_TEMP_ERROR: 70,
        CPU_TEMP_FATAL: 80
    },
    KEY_OPTIONS: {
        "inChina": False,
        "cli_enabled": False
    },
    KEY_URLS: {
        "server": f'{SERVER_IP}:5000',
        "denva": f"{DENVA_IP}:5000",
        KEY_DENVA_TWO: f"{DENVA_TWO_IP}:5000",
        "dump1090_data": f"{DENVA_IP}:16601/data.json"
    },
    KEY_LATENCY: {
        "max": 200,
        "max-slow": 1000,
        "five-seconds": 5000,
    },
    KEY_LOGS: {
        'dev_app': f'{PI_CONFIG_PATH}dev_log_app_config.json',
        'dev_ui': f'{PI_CONFIG_PATH}dev_log_ui_config.json',
        'dev_ddd': f'{PI_CONFIG_PATH}dev_log_ddd_config.json',
        'server_app': f'{PI_CONFIG_PATH}server_log_app_config.json',
        'server_ui': f'{PI_CONFIG_PATH}server_log_ui_config.json',
        'denva_app': f'{PI_CONFIG_PATH}log_app_config.json',
        'denva_ui': f'{PI_CONFIG_PATH}log_ui_config.json',
        'hc': f'{PI_CONFIG_PATH}log_config.json',
        'log_app': f'{PI_LOGS_PATH}logs.log',
        'log_hc': f'{PI_LOGS_PATH}healthcheck.log',
        'log_ui': f'{PI_LOGS_PATH}server.log',
        'ddd': f'{PI_CONFIG_PATH}log_ddd_config.log',
        'overseer_mode': f'{PI_CONFIG_PATH}overseer_mode.json',
        'overseer': f'{PI_CONFIG_PATH}overseer.json',
    },
    "informationData": f'{PI_DATA_PATH}information.json',
    "test": {
        'slow_test': False
    },
    MEASUREMENT_LIST_SIZE: 2000
}


def get_log_path_for(log_type: str) -> str:
    return settings[KEY_LOGS][log_type]


# TODO REFACTOR
def get_environment_log_path_for(where: str) -> str:
    env_type = settings['mode']
    if where == 'denva_app':
        return f'{PI_CONFIG_PATH}log_denva_app_config.json'
    if where == 'overseer_mode':
        return settings[KEY_LOGS]['overseer_mode']
    if where == 'overseer':
        return settings[KEY_LOGS]['overseer']
    if where == 'cctv':
        return settings[KEY_LOGS]['cctv']
    if where == 'hc':
        return settings[KEY_LOGS]['hc']

    if where == 'ddd':
        return settings[KEY_LOGS]['dev_' + where]

    if env_type == 'dev':
        return settings[KEY_LOGS]['dev_' + where]
    print(settings[KEY_LOGS]['{}_{}'.format(env_type, where)])
    return settings[KEY_LOGS]['{}_{}'.format(env_type, where)]


def get_information_path() -> str:
    return settings['informationData']


def load_cfg() -> dict:
    return settings.copy()


def get_healthcheck_ip() -> str:
    config = load_cfg()
    return config[KEY_SYSTEM]['ip']


def get_current_warnings_url_for(service: str) -> str:
    config = load_cfg()
    return "{}/warns/now".format(config['urls'][service])


def get_options() -> dict:
    config = load_cfg()
    return config['options']


def get_path_for_personal_events() -> str:
    return settings[KEY_PATH]['events']


def get_path_for_backup() -> str:
    return settings[KEY_PATH]['backup']


def get_path_to_chinese_dictionary() -> str:
    return settings[KEY_PATH]['chinese-dictionary']


def get_irregular_verbs_path() -> str:
    return f'{PI_KNYSZOGAR_DATA}irregular_verbs.txt'


def set_mode_to(mode: str):
    settings['mode'] = mode
    print('The mode is set to {}'.format(settings['mode']))


def get_mode() -> str:
    return settings['mode']


def get_memory_available_threshold():
    return settings[KEY_SYSTEM]['memory_available']


def get_disk_space_available_threshold():
    return settings[KEY_SYSTEM]['free_space']


def run_slow_test() -> bool:
    return settings['test']['slow_test']


def get_shaking_level():
    return settings[KEY_SENSORS]['motion']['shaking']


def get_sensitivity():
    return settings[KEY_SENSORS]['motion']['sensitivity']


def get_sensor_log_file_for(year: int, month: int, day: int, sensor_filename: str = 'sensor-log') -> str:
    path = PI_LOGS_PATH + dom_utils.get_filename_from_year_month_day(sensor_filename, 'csv', year, month, day)
    return path


def get_metrics_service_url():
    return settings[KEY_URLS]["server"] + "/metrics/add"


def get_warm_up_measurement_counter():
    return settings[KEY_SENSORS]['bme']['warm_up']


def get_radar_hc_url() -> str:
    return settings[KEY_URLS]["denva"] + "/hc/ar"


def get_system_hc_url() -> str:
    return settings[KEY_URLS]["server"] + "/shc/update"


def get_system_hc_reboot_url() -> str:
    return settings[KEY_URLS]["server"] + "/shc/reboot"


def get_service_on_off_url() -> str:
    return settings[KEY_URLS]["server"] + "/shc/change"


def get_directory_path_for_aircraft() -> str:
    return PI_DATA_PATH


def get_url_for_dump1090():
    return settings[KEY_URLS]["dump1090_data"]


def max_latency(fast: bool = True):
    if fast:
        return settings[KEY_LATENCY]["max"]
    return settings[KEY_LATENCY]["max-slow"]


def slow_latency():
    return settings[KEY_LATENCY]["five-seconds"]


def get_system_hc() -> str:
    return str(Path(f'{PI_DATA_PATH}/hc.json'))


def get_default_brightness_for_unicornhd_display():
    return settings[KEY_SENSORS]["unicornhd"]["default_brightness"]


def is_cctv_camera_on() -> bool:
    return settings[KEY_SENSORS]["cameras"]["cctv"]


def is_sky_camera_on() -> bool:
    return settings[KEY_SENSORS]["cameras"]["sky"]


def is_radar_on():
    return settings[KEY_SENSORS]["radar"]


def get_overseer_mode_file_path():
    return settings[KEY_PATH]["overseer_mode"]


def get_path_to_text():
    return settings[KEY_PATH]["text"]


def get_post_denva_measurement_url(which: str = 'one'):
    return f'{SERVER_IP}:5000/measurement/denva/{which}'


def get_add_diary_entry_url():
    return f'{SERVER_IP}:5000/diary/add'


def get_warnings_path_for(date) -> str:
    return f'{PI_DATA_PATH}{dom_utils.get_date_as_folders_for(date)}warnings.txt'


def get_warnings_path_for_today() -> str:
    return f'{PI_DATA_PATH}{dom_utils.get_date_as_folders_for_today()}warnings.txt'


def get_slow_refresh_rate():
    return settings[REFRESH_RATE]['slow']


def get_normal_refresh_rate():
    return settings[REFRESH_RATE]['normal']


def get_fast_refresh_rate():
    return settings[REFRESH_RATE]['fast']


def get_measurement_size():
    return settings[MEASUREMENT_LIST_SIZE]


def get_url_for_denva():
    return settings[KEY_URLS]['denva']


def get_url_for_denva_two():
    return settings[KEY_URLS]['denva2']


def get_today_warnings():
    return settings[KEY_PATH]['all_warnings']


def get_healthcheck_path():
    return settings[KEY_PATH]['healthcheck']


def reload_config_from_file():
    global settings
    result = data_files.load_json_data_as_dict_from('config.json')
    if 'error' in result:
        return result
    else:
        settings = result.copy()
        return result


def is_cli_mode_enabled():
    return settings[KEY_OPTIONS]['cli_enabled']
