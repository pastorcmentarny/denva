import csv
import datetime
import logging
import os
import sys
import time

import bme680
# from threading import Thread
import smbus
import veml6075
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from bh1745 import BH1745
from icm20948 import ICM20948
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

# file setup
original = os.getcwd()
os.chdir('/home/pi/')
log_file = os.getcwd() + '/denva-log.txt'
sensor_file = os.getcwd() + '/sensor-log.csv'
os.chdir(original)


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file)

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

samples = []
points = []

sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()

sensitivity = 8


# Function to thread accelerometer values separately to OLED drawing

def sample():
    for i in range(51):
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz

        v = ay  # Change this axis depending on orientation of breakout

        # Scale up or down depending on sensitivity required

        v *= (100 * sensitivity)

        points.append(v)
        if len(points) > 100:
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
    return 'Acc: {:5.1f} {:5.1f} {:5.0f} Gyro: {:5.1f} {:5.1f} {:5.1f} Mag: {:5.1f} {:5.1f} {:5.1f}'.format(motion['ax'],
                                                                                                            motion['ay'],
                                                                                                            motion['az'],
                                                                                                            motion['gx'],
                                                                                                            motion['gy'],
                                                                                                            motion['gz'],
                                                                                                            motion['mx'],
                                                                                                            motion['my'],
                                                                                                            motion['mz'])


def display_measurement_time(start_time, end_time):
    result = end_time.microsecond - start_time.microsecond
    logging.debug('it took ' + str(result) + ' microseconds to measure it.')


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
        get_motion_as_string(motion))
    logging.info(measurement)
    print_measurement(data, 20, 6)
    timestamp = datetime.datetime.now()
    sensor_log_file = open(sensor_file, 'a+', newline='')
    csv_writer = csv.writer(sensor_log_file)
    csv_writer.writerow([timestamp,
                         data['temp'], data['pressure'], data['humidity'], data['gas_resistance'],
                         data['colour'], data['aqi'],
                         data['uva_index'], data['uvb_index'],
                         data['motion'],
                         motion['ax'], motion['ay'], motion['az'],
                         motion['gx'], motion['gy'], motion['gz'],
                         motion['mx'], motion['my'], motion['mz']
                         ])
    sensor_log_file.close()


def print_measurement(data, left_width, right_width):
    print_title(left_width, right_width)
    print_items(data, left_width, right_width)
    print('-'*20 + '\n')


def print_items(data, left_width, right_width):
    for k, v in data.items():
        print(k.ljust(left_width, '.') + str(v).rjust(right_width, ' '))


def print_title(left_width, right_width):
    title = 'Measurement @ {}'.format(datetime.datetime.now())
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
    if motion > 1000:
        for i in range(5):
            bh1745.set_leds(1)
            time.sleep(0.2)
            bh1745.set_leds(0)
            time.sleep(0.05)


def get_brightness(r, g, b) -> str:
    max_value = max(r, g, b)
    mid = (r+g+b)/3
    result = (max_value+mid)/2

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


def main():

    while True:
        try:
            logging.debug('getting measurement')
            start_time = datetime.datetime.now()

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

            end_time = datetime.datetime.now()
            data = {
                "temp": temp,
                "pressure": pressure,
                "humidity": humidity,
                "gas_resistance": gas_resistance,
                "aqi": aqi,
                "colour": colour,
                "motion": motion,
                "uva_index": uva_index,
                "uvb_index": uvb_index
            }

            store_measurement(data)

            display_measurement_time(start_time, end_time)

            img = Image.open("images/background.png").convert(oled.mode)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (128, 128)], fill="black")
            draw.text((0, 0), "Temp: {}".format(temp), fill="white", font=rr_12)
            draw.text((0, 14), "Pressure: {}".format(pressure), fill="white", font=rr_12)
            draw.text((0, 28), "Humidity: {}".format(humidity), fill="white", font=rr_12)
            draw.text((0, 42), "Colour: {}".format(colour), fill="white", font=rr_12)
            draw.text((0, 56), "Brightness: {}".format(get_brightness(r, g, b)), fill="white", font=rr_12)
            draw.text((0, 70), "Motion: {:05.02f}".format(motion), fill="white", font=rr_12)
            draw.text((0, 84), "UVA: {}".format(uv_description(uva_index)), fill="white", font=rr_12)
            draw.text((0, 98), "UVB: {}".format(uv_description(uvb_index)), fill="white", font=rr_12)
            oled.display(img)

        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            sys.exit(0)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    bh1745.set_leds(0)
    main()
