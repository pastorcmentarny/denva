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
import logging.config
import os
import sys
import time
import traceback
from datetime import datetime
from timeit import default_timer as timer

import smbus
from PIL import ImageFont

import config
import dom_utils
from common import data_files, commands
from denva import cl_display, denva_sensors_service
from emails import email_sender_service
from gateways import local_data_gateway
from sensors import air_quality_service, environment_service, gps_sensor, co2_sensor, two_led_service

bus = smbus.SMBus(1)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

samples = []
pictures = []

logger = logging.getLogger('app')
warnings_logger = logging.getLogger('warnings')

app_startup_time = datetime.now()

counter = 1
led_status = 0


def get_data_from_measurement() -> dict:
    environment = environment_service.get_measurement()
    eco2 = ""
    tvoc = ""
    try:
        eco2 = air_quality_service.get_eco2_measurement_as_string()
        tvoc = air_quality_service.get_tvoc_measurement_as_string()
        local_data_gateway.post_metrics_update('air_quality', 'ok')
    except Exception as air_quality_exception:
        logger.error(f'Unable to read from air quality sensor due to {air_quality_exception}')
        local_data_gateway.post_metrics_update('air_quality', 'errors')

    red, green, blue = two_led_service.get_measurement()
    colour = dom_utils.to_hex(red, green, blue)

    try:
        gps_data = gps_sensor.get_measurement()
    except Exception as get_data_exception:
        gps_data = {'timestamp': datetime.time(0, 0, 0), 'latitude': 0.0, 'longitude': -0.0,
                    'altitude': 0, 'lat_dir': 'N', 'lon_dir': 'W', 'geo_sep': '0', 'num_sats': '0', 'gps_qual': 0,
                    'speed_over_ground': 0.0, 'mode_fix_type': '0', 'pdop': '0', 'hdop': '0', 'vdop': '0',
                    '_i2c_addr': 16, '_i2c': 'x', '_debug': False, "error": str(get_data_exception)}

    co2_data = co2_sensor.get_measurement()
    return {
        "temp": environment['temp'], "pressure": environment['pressure'], "humidity": environment['humidity'],
        "gas_resistance": "{:.2f}".format(environment['gas_resistance']),
        "colour": colour,
        "r": red, "g": green, "b": blue,
        "eco2": eco2, "tvoc": tvoc,
        'gps_latitude': gps_data['latitude'], 'gps_longitude': gps_data['longitude'],
        'gps_altitude': gps_data['altitude'],
        'gps_lat_dir': gps_data['lat_dir'], 'gps_lon_dir': gps_data['lon_dir'], 'gps_geo_sep': gps_data['geo_sep'],
        'gps_num_sats': gps_data['num_sats'], 'gps_qual': gps_data['gps_qual'],
        'gps_speed_over_ground': gps_data['speed_over_ground'], 'gps_mode_fix_type': gps_data['mode_fix_type'],
        'gps_pdop': gps_data['pdop'], 'gps_hdop': gps_data['hdop'], 'gps_vdop': gps_data['vdop'],
        "co2": co2_data[0],
        "co2_temperature": co2_data[1],
        "relative_humidity": co2_data[2]
    }


def main():
    measurement_counter = 0
    two_led_service.led_startup_show()
    while True:
        measurement_counter += 1
        logger.debug('Getting measurement no.{}'.format(measurement_counter))
        start_time = timer()
        data = get_data_from_measurement()
        data['cpu_temp'] = commands.get_cpu_temp()
        end_time = timer()
        measurement_time = int((end_time - start_time) * 1000)  # in ms

        logger.info('Measurement no. {} took {} milliseconds to measure it.'
                    .format(measurement_counter, measurement_time))

        data['measurement_counter'] = measurement_counter
        data['measurement_time'] = str(measurement_time)
        data_files.store_measurement(data, denva_sensors_service.get_sensor_log_file(),
                                     denva_sensors_service.get_sensor_log_file_at_server())

        cl_display.print_measurement(data)
        local_data_gateway.post_denva_measurement(data)
        if measurement_counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('denva', 'app')

        remaining_of_five_s = 5 - (float(measurement_time) / 1000)

        if measurement_time > config.max_latency(fast=False):
            logger.warning("Measurement {} was slow.It took {} ms".format(measurement_counter, measurement_time))

        if remaining_of_five_s > 0:
            time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements


def cleanup_before_exit():
    two_led_service.on()
    sys.exit(0)


if __name__ == '__main__':
    global points
    config.set_mode_to('denva')
    data_files.setup_logging(config.get_environment_log_path_for('denva_app'))
    logger.info('Starting application ... \n Press Ctrl+C to shutdown')
    email_sender_service.send_ip_email('denva')
    try:
        logging.info('Mounting network drives')
        commands.mount_all_drives()

        logging.info("Sensor warming up, please wait...")
        air_quality_service.start_measurement()
        logging.info('Sensor needed {} seconds to warm up'.format(counter))
        two_led_service.off()
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        cleanup_before_exit()
    except Exception as exception:
        print(f'Whoops. {exception}')
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(exception))
        cleanup_before_exit()
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
        cleanup_before_exit()
