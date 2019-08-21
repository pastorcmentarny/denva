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

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

samples = []
points = []
pictures = []


sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()

sensitivity = 8
shaking_level = 1000
cycle = 0

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
            time.sleep(0.2)
            bh1745.set_leds(0)
            time.sleep(0.05)


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
    aqi = 0
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


def main():
    led_startup_show()
    global cycle
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

            data['picture_path'] = pictures

            email_sender_service.should_send_email(data)
            email_sender_service.should_send_report_email()

            remaining_of_five_s = 5 - (float(measurement_time) / 1000)

            if remaining_of_five_s > 0:
                time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements

        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            bh1745.set_leds(0)
            sys.exit(0)


def thread_camera():
    while True:
        time.sleep(15)
        last_picture = commands.capture_picture()
        if last_picture != "":
            pictures.append(last_picture)
            if len(pictures) > 5:
                pictures.pop(0)


if __name__ == '__main__':
    data_files.setup_logging()

    print('Starting application ... \n Press Ctrl+C to shutdown')
    try:
        camera_thread = threading.Thread(target=thread_camera)
        camera_thread.start()
        main()
    except Exception:
        logger.error('Something went badly wrong..', exc_info=True)
        bh1745.set_leds(1)
        sys.exit(0)
