#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import json
import logging
import logging.config
import os
import subprocess
import sys
import time
import re

import bme680
import smbus
import veml6075
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from bh1745 import BH1745
from icm20948 import ICM20948
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

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
bh1745.set_leds(1)

# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')

# Set up motion sensor
imu = ICM20948()

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

samples = []
points = []

sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()

sensitivity = 8
shaking_level = 1000
logger = logging.getLogger('app')
warnings_logger = logging.getLogger('warnings')


def setup_logging(default_path='log_config.json', default_level=logging.DEBUG, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as config_json_file:
            config = json.load(config_json_file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_sensor_log_file() -> str:
    today = datetime.datetime.now()
    return '/home/pi/logs/sensor-log' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'


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


def get_motion_as_string(motion: dict) -> str:
    return 'Acc: {:5.1f} {:5.1f} {:5.0f} Gyro: {:5.1f} {:5.1f} {:5.1f} Mag: {:5.1f} {:5.1f} {:5.1f}'.format(
        motion['ax'],
        motion['ay'],
        motion['az'],
        motion['gx'],
        motion['gy'],
        motion['gz'],
        motion['mx'],
        motion['my'],
        motion['mz'])


def get_measurement_time(start_time, end_time):
    return end_time.microsecond - start_time.microsecond


def get_warnings(data) -> list:
    warnings = []
    if data['temp'] < 16:
        warnings.append("Temp. is TOO LOW")
        warnings_logger.error('Temperature is too low. Current temperature is: ' + str(data['temp']))
    elif data['temp'] < 18:
        warnings.append("Temp. is low")
        warnings_logger.warning('Temperature is low. Current temperature is: ' + str(data['temp']))
    elif data['temp'] > 25:
        warnings.append("Temp. is high")
        warnings_logger.warning('Temperature is high. Current temperature is: ' + str(data['temp']))
    elif data['temp'] > 30:
        warnings.append("Temp. is TOO HIGH")
        warnings_logger.error('Temperature is too high. Current temperature is: ' + str(data['temp']))

    if data['humidity'] < 30:
        warnings.append("Humidity is TOO LOW")
        warnings_logger.error('Humidity is too low. Current humidity is: ' + str(data['humidity']))
    elif data['humidity'] < 40:
        warnings.append("Humidity is low")
        warnings_logger.warning('Humidity is low. Current humidity is: ' + str(data['humidity']))
    elif data['humidity'] > 60:
        warnings.append("Humidity is high")
        warnings_logger.warning('Humidity is high. Current humidity is: ' + str(data['humidity']))
    elif data['humidity'] > 70:
        warnings.append("Humidity is TOO HIGH")
        warnings_logger.error('Humidity is too high. Current humidity is: ' + str(data['humidity']))

    if data['uva_index'] > 6:
        warnings.append("UV A is TOO HIGH")
        warnings_logger.error('UV A is too high. Current UV A is: ' + str(data["uva_index"]))

    if data['uvb_index'] > 6:
        warnings.append("UV B is TOO HIGH")
        warnings_logger.error('UV B is too high. Current UV B is: ' + str(data["uvb_index"]))

    if data['motion'] > shaking_level:
        warnings_logger.info('Dom is shaking his legs. Value: ' + str(data["motion"]))

    if data['cpu_temp'] > 75:
        warnings.append("CPU temp. TOO HIGH!")
        warnings_logger.error('CPU temperature is too high. Current temperature is: ' + str(data['temp']))
    elif data['cpu_temp'] > 60:
        warnings.append("CPU temp. VERY HIGH")
        warnings_logger.error('CPU temperature is very high. Current temperature is: ' + str(data['temp']))
    elif data['cpu_temp'] > 50:
        warnings.append("CPU temp. is high")
        warnings_logger.warning('CPU temperature is high. Current temperature is: ' + str(data['temp']))


    return warnings


def get_cpu_temp():
    return str(subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']), "utf-8") \
        .replace('temp=', 'CPU:')


def get_cpu_speed():
    cmd = "find /sys/devices/system/cpu/cpu[0-3]/cpufreq/scaling_cur_freq -type f | xargs cat | sort | uniq -c"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = str(output)
    output = output.strip()[4:len(output) - 3].strip()[2:]  # i am sorry ..
    try:
        output = str(float(output) / 1000)
    except ValueError:
        logging.warning(output)
        return 'CPU: variable speed'
    return 'CPU: ' + output + ' Mhz'


def store_measurement(data):
    motion = get_current_motion_difference()
    measurement = 'temp: {} pressure: {} humidity: {} gas_resistance {}, colour: {} AQI: {} UVA: {} UVB: {} motion: {} motion diff: {}'.format(
        data['temp'],
        data['pressure'],
        data['humidity'],
        data['gas_resistance'],
        data['colour'],
        data['aqi'],
        data['uva_index'],
        data['uvb_index'],
        data['motion'],
        get_motion_as_string(motion),
        data["cpu_temp"],
        str(data['measurement_time']) + ' ms.')
    logging.info(measurement)
    print_measurement(data, 20, 6)
    timestamp = datetime.datetime.now()
    sensor_log_file = open(get_sensor_log_file(), 'a+', newline='')
    csv_writer = csv.writer(sensor_log_file)
    csv_writer.writerow([timestamp,
                         data['temp'], data['pressure'], data['humidity'], data['gas_resistance'],
                         data['colour'], data['aqi'],
                         data['uva_index'], data['uvb_index'],
                         data['motion'],
                         motion['ax'], motion['ay'], motion['az'],
                         motion['gx'], motion['gy'], motion['gz'],
                         motion['mx'], motion['my'], motion['mz'],
                         data['measurement_time'],
                         get_cpu_from_text(data['cpu_temp'])
                         ])
    sensor_log_file.close()


def get_cpu_from_text(cpu_temp:str):
    return re.sub('[^0-9.]', '', cpu_temp)


def get_ip():
    text = str(subprocess.check_output(['ifconfig', 'wlan0']), "utf-8")
    start, end = text.find('inet'), text.find('netmask')
    result = text[start+4: end]
    return 'IP:' + result.strip()


def print_measurement(data, left_width, right_width):
    print_title(left_width, right_width)
    print_items(data, left_width, right_width)
    print('-' * 36 + '\n')


def print_items(data, left_width, right_width):
    for title, value in data.items():
        print(title.ljust(left_width, '.') + str(value).rjust(right_width, ' '))


def print_title(left_width, right_width):
    title = 'Measurement @ {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(title.center(left_width + right_width, "-"))


def uv_description(uv_index):
    if uv_index == 0:
        return "NONE"
    elif uv_index < 3:
        return "LOW"
    elif 3 <= uv_index < 6:
        return "MEDIUM"
    elif 6 <= uv_index < 8:
        return "HIGH"
    elif 8 <= uv_index < 11:
        return "VERY HIGH"
    elif uv_index > 11:
        return "EXTREME"
    else:
        logging.warning('weird uv value: {}'.format(uv_index))
        return "UNKNOWN"


def warn_if_dom_shakes_his_legs(motion):
    if motion > shaking_level:
        for i in range(5):
            bh1745.set_leds(1)
            time.sleep(0.2)
            bh1745.set_leds(0)
            time.sleep(0.05)


def get_brightness(r, g, b) -> str:
    max_value = max(r, g, b)
    mid = (r + g + b) / 3
    result = (max_value + mid) / 2

    if result < 16:
        return 'pitch black'
    elif 32 <= result < 64:
        return 'very dark'
    elif 64 <= result < 96:
        return 'dark'
    elif 96 <= result < 128:
        return 'bit dark'
    elif 128 <= result < 160:
        return 'grey'
    elif 160 <= result < 192:
        return 'bit bright'
    elif 192 <= result < 224:
        return 'bright'
    elif 224 <= result < 240:
        return 'very bright'
    elif 240 <= result < 256:
        return 'white'
    else:
        logging.warning('weird brightness value: {} for {} {} {}'.format(result, r, g, b))
        return '?'


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
    aqi = 0
    r, g, b = bh1745.get_rgb_scaled()
    colour = '#{:02x}{:02x}{:02x}'.format(r, g, b)
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


def main():
    bh1745.set_leds(0)
    while True:
        try:
            logging.debug('getting measurement')

            start_time = datetime.datetime.now()
            data = get_data_from_measurement()
            end_time = datetime.datetime.now()

            data['cpu_temp'] = get_cpu_temp()
            measurement_time = get_measurement_time(start_time, end_time)
            data['measurement_time'] = measurement_time
            store_measurement(data)
            logging.debug('it took ' + str(measurement_time) + ' microseconds to measure it.')

            draw_image_on_screen(data)

            time.sleep(2)  # wait at least few seconds between measurements

        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            bh1745.set_leds(0)
            sys.exit(0)


def get_uptime():
    return str(subprocess.check_output(['uptime', '-p']), "utf-8") \
        .replace('days', 'd') \
        .replace('day', 'd') \
        .replace('hours', 'h') \
        .replace('hour', 'h') \
        .replace('minutes', 'm') \
        .replace('minute', 'm')


swapped = False
warning_swap = False
cycle = 0


def draw_image_on_screen(data):
    global swapped
    global warning_swap
    global cycle
    cycle += 1

    warnings = get_warnings(data)
    img = Image.open("/home/pi/denva-master/src/images/background.png").convert(oled.mode)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (128, 128)], fill="black")
    if len(warnings) > 0 and warning_swap:
        draw.text((0, 0), "WARNINGS", fill="white", font=rr_14)
        y = 2
        for warning in warnings:
            y += 14
            draw.text((0, y), warning, fill="white", font=rr_12)
    else:
        draw.text((0, 0), "Temp: {}".format(data["temp"]), fill="white", font=rr_12)
        draw.text((0, 14), "Pressure: {}".format(data["pressure"]), fill="white", font=rr_12)
        draw.text((0, 28), "Humidity: {}".format(data["humidity"]), fill="white", font=rr_12)
        draw.text((0, 42), "Motion: {:05.02f}".format(data["motion"]), fill="white", font=rr_12)
        if swapped:
            draw.text((0, 56), "Colour: {}".format(data["colour"]), fill="white", font=rr_12)
            draw.text((0, 70), "UVA: {}".format(uv_description(data["uva_index"])), fill="white", font=rr_12)
        else:
            draw.text((0, 56), "Brightness: {}".format(get_brightness(data["r"], data["g"], data["b"])), fill="white",
                      font=rr_12)
            draw.text((0, 70), "UVB: {}".format(uv_description(data["uvb_index"])), fill="white", font=rr_12)
        swapped = not swapped

    #  system line (TODO change every 5 cycles)

    if cycle % 4 == 0:
        draw.text((0, 84), get_cpu_temp(), fill="white", font=rr_12)
    elif cycle % 4 == 1:
        draw.text((0, 84), get_uptime(), fill="white", font=rr_12)
    elif cycle % 4 == 3:
        draw.text((0, 84), get_ip(), fill="white", font=rr_12)
    else:
        draw.text((0, 84), get_cpu_speed(), fill="white", font=rr_12)

    oled.display(img)
    warning_swap = not warning_swap  # //FIXME improve it

    if cycle > 12:
        cycle = 0


if __name__ == '__main__':
    setup_logging()

    print('Starting application ... \n Press Ctrl+C to shutdown')
    try:
        main()
    except Exception:
        logger.error('Something went badly wrong..', exc_info=True)
        bh1745.set_leds(0)
        sys.exit(0)
