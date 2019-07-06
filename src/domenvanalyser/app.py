import csv
import datetime
import logging
import os
import sys
import time
from threading import Thread
import smbus
import bme680
import veml6075
from bh1745 import BH1745
from icm20948 import ICM20948

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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

sensitivity = 8  # Value from 1 to 10. Determines twitchiness of needle


# Function to thread accelerometer values separately to OLED drawing

def sample():
    while True:
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

        time.sleep(0.05)

# The thread to measure accelerometer values


t = Thread(target=sample)
t.start()


def get_motion():
    value = 0
    for i in range(1, len(points)):
        value += abs(points[i] - points[i - 1])
    return value


def get_current_motion_difference() -> str:
    x, y, z = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

    ax -= sx
    ay -= sy
    az -= sz

    return 'Acc: {:05.2f} {:03.0f} {:05.2f} Gyro:  {:05.2f} {:05.2f} {:05.2f} Mag:   {:05.2f} {:05.2f} {:05.2f}'.format(    ax, ay, az, gx, gy, gz, x, y, z)


def display_measurement_time(start_time, end_time):
    result = end_time.microsecond - start_time.microsecond
    logging.debug('it took ' + str(result) + ' microseconds to measure it.')


def store_measurement(temp, pressure, humidity, gas_resistance, colour, aqi, uva_index, uvb_index, motion):
    measurement = 'temp: {} pressure: {} humidity: {} gas_resistance {}, colour: {} AQI: {} UVA: {} UVB: {} motion: {} motion diff: {}'.format(
        temp, pressure, humidity, gas_resistance, colour, aqi, uv_description(uva_index),
        uv_description(uvb_index), motion, get_current_motion_difference())
    logging.info(measurement)
    print(measurement)

    timestamp = datetime.datetime.now()
    sensor_log_file = open(sensor_file, 'a+', newline='')
    csv_writer = csv.writer(sensor_log_file)
    csv_writer.writerow([timestamp, temp, pressure, humidity, colour, aqi, uva_index, uvb_index, motion])
    sensor_log_file.close()


def uv_description(uv_index):
    if uv_index < 3:
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
        return "UNKNOWN"


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

            uva, uvb = uv_sensor.get_measurements()
            uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
            uv_indices = uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)
            uva_index, uvb_index, avg_uv_index = uv_indices

            end_time = datetime.datetime.now()

            store_measurement(temp, pressure, humidity, gas_resistance, colour, aqi, uva, uvb, motion)

            display_measurement_time(start_time, end_time)

            img = Image.open("images/background.png").convert(oled.mode)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (128, 128)], fill="black")
            draw.text((0, 0), "UVA: {:02.01f}".format(uva_index), fill="white", font=rr_12)
            draw.text((0, 14), "UVB: {:02.01f}".format(uvb_index), fill="white", font=rr_12)
            draw.text((0, 28), "Temp: {}".format(temp), fill="white", font=rr_12)
            draw.text((0, 42), "Pressure: {}".format(pressure), fill="white", font=rr_12)
            draw.text((0, 56), "Humidity: {}".format(humidity), fill="white", font=rr_12)
            draw.text((0, 70), "Colour: {}".format(colour), fill="white", font=rr_12)
            draw.text((0, 84), "Motion: {}".format(motion), fill="white", font=rr_12)
            oled.display(img)

            time.sleep(1)  # wait for one second
        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            sys.exit(0)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    bh1745.set_leds(0)
    main()
