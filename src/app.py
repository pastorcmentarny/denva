#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import logging.config
import os
import sys
import threading
import time
from timeit import default_timer as timer

import bme680
import smbus
import veml6075

from PIL import ImageFont
from bh1745 import BH1745
from icm20948 import ICM20948
from sgp30 import SGP30

import app_timer
import cl_display
import commands
import data_files
import email_sender_service
import mini_display
import utils

TEMP_OFFSET = 0.0

bus = smbus.SMBus(1)

# Set up weather sensor
weather_sensor = bme680.BME680()
weather_sensor.set_humidity_oversample(bme680.OS_2X)
weather_sensor.set_pressure_oversample(bme680.OS_4X)
weather_sensor.set_temperature_oversample(bme680.OS_8X)
weather_sensor.set_filter(bme680.FILTER_SIZE_3)
weather_sensor.set_temp_offset(TEMP_OFFSET)

# Set up light sensor
bh1745 = BH1745()
bh1745.setup()

# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')

# Set up motion sensor
imu = ICM20948()

# air quality
sgp30 = SGP30()


rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

samples = []
points = []
pictures = []


sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()

sensitivity = 8
shaking_level = 1000

logger = logging.getLogger('app')
warnings_logger = logging.getLogger('warnings')

app_startup_time = datetime.now()


def sample():
    for i in range(51):
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz

        v = ay  # Change this axis depending on orientation of breakout

        v *= (100 * sensitivity)

        points.append(v)
        if len(points) > 50:
            points.pop(0)

        time.sleep(0.01)


def get_motion():
    sample()
    value = 0
    for i in range(1, len(points)):
        value += abs(points[i] - points[i - 1])
    return value


def get_current_motion_difference() -> dict:
    mx, my, mz = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

    ax -= sx
    ay -= sy
    az -= sz
    return {
        'ax': ax, 'ay': ay, 'az': az,
        'gx': gx, 'gy': gy, 'gz': gz,
        'mx': mx, 'my': my, 'mz': mz
    }


def warn_if_dom_shakes_his_legs(motion):
    if motion > shaking_level:
        for i in range(5):
            bh1745.set_leds(1)
            time.sleep(0.25)
            bh1745.set_leds(0)
            time.sleep(0.15)


def get_data_from_measurement():
    temp = 0
    pressure = 0
    humidity = 0
    gas_resistance = 0
    if weather_sensor.get_sensor_data():
        temp = weather_sensor.data.temperature
        pressure = weather_sensor.data.pressure
        humidity = weather_sensor.data.humidity
        gas_resistance = weather_sensor.data.gas_resistance
    else:
        logger.warning("Weather sensor did't return data")
    aqi = sgp30.get_air_quality()
    r, g, b = bh1745.get_rgb_scaled()
    colour = utils.to_hex(r, g, b)
    motion = get_motion()
    warn_if_dom_shakes_his_legs(motion)

    uva, uvb = uv_sensor.get_measurements()
    uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
    uv_indices = uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)
    uva_index, uvb_index, avg_uv_index = uv_indices

    return {
        "temp": temp,
        "pressure": pressure,
        "humidity": humidity,
        "gas_resistance": "{:.2f}".format(gas_resistance),
        "aqi": aqi,
        "colour": colour,
        "motion": motion,
        "uva_index": uva_index,
        "uvb_index": uvb_index,
        "r": r,
        "g": g,
        "b": b,
    }


def led_startup_show():
    bh1745.set_leds(1)
    time.sleep(0.3)
    bh1745.set_leds(0)
    time.sleep(0.2)
    bh1745.set_leds(1)
    time.sleep(0.25)
    bh1745.set_leds(0)
    time.sleep(0.15)
    bh1745.set_leds(1)
    for i in range(5):
        bh1745.set_leds(1)
        time.sleep(0.2)
        bh1745.set_leds(0)
        time.sleep(0.1)
    bh1745.set_leds(0)


def get_pictures_path():
    p = []
    if len(pictures) > 2:
        p = [pictures[0], pictures[-1]]
    elif len(pictures) == 1:
        p = [pictures[0]]
    return p


def main():
    led_startup_show()
    while True:
        try:
            logger.debug('getting measurement')
            start_time = timer()
            data = get_data_from_measurement()
            data['cpu_temp'] = commands.get_cpu_temp()
            end_time = timer()

            measurement_time = str(int((end_time - start_time) * 1000))  # in ms
            data['measurement_time'] = measurement_time
            data_files.store_measurement(data, get_current_motion_difference())
            logger.debug('it took ' + str(measurement_time) + ' microseconds to measure it.')

            cl_display.print_measurement(data)
            mini_display.draw_image_on_screen(data, app_timer.get_app_uptime(app_startup_time))



            data['picture_path'] = get_pictures_path()

            email_sender_service.should_send_email(data)
            email_sender_service.should_send_report_email()

            remaining_of_five_s = 5 - (float(measurement_time) / 1000)

            if remaining_of_five_s > 0:
                time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements

        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            bh1745.set_leds(0)
            cleanup_before_exit()


def thread_camera():
    logger.info('Starting taking picture thread..', exc_info=True)
    while True:
        time.sleep(5)
        last_picture = commands.capture_picture()
        if last_picture != "":
            pictures.append(last_picture)
            if len(pictures) > 5:
                pictures.pop(0)


counter = 1
led_status = 0

def crude_progress_bar():
    global counter
    global  led_status
    sys.stdout.write('Waiting.. ' + str(counter) + 's.\n')
    counter = counter+1
    sys.stdout.flush()
    bh1745.set_leds(led_status)
    if led_status == 1:
        led_status = 0
    else:
        led_status = 1

def cleanup_before_exit():
    camera_thread.join()
    sys.exit(0)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    data_files.setup_logging()
    try:
        commands.mouth_drive()
        camera_thread = threading.Thread(target=thread_camera)
        camera_thread.start()
        print("Sensor warming up, please wait...")
        logger.info('Sensor warming up, please wait...')
        sgp30.start_measurement(crude_progress_bar)
        sys.stdout.write('\n')
        logger.info('Sensor needed {} seconds to warm up')
        bh1745.set_leds(0)
        main()
    except Exception as e:
        logger.error('Something went badly wrong..', exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(e))
        bh1745.set_leds(1)

        cleanup_before_exit()
