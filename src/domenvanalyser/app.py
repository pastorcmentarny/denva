import csv
import datetime
import logging
import os
import sys
import time
import smbus
import veml6075
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

os.chdir('/home/pi')

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename=os.getcwd() + 'denva-log.txt')

bus = smbus.SMBus(1)

# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_15 = ImageFont.truetype(rr_path, 15)


def display_measurement_time(start_time, end_time):
    result = end_time.microsecond - start_time.microsecond
    logging.debug('it took ' + str(result) + ' microseconds to measure it.')


def store_measurement(temp, pressure, humidity, luminance, colour, aqi, uva_index, uvb_index, motion):
    measurement = 'temp: {} pressure: {} humidity: {} luminace: {} colour: {} AQI: {} UVA: {} UVB: {} motion: {}'.format(
        temp, pressure, humidity, luminance, colour, aqi, uv_description(uva_index), uv_description(uvb_index), motion)
    logging.info(measurement)
    print(measurement)

    timestamp = datetime.datetime.now()
    sensor_log_file = open(os.getcwd() + 'sensor-log.csv', 'a+', newline='')
    csv_writer = csv.writer(sensor_log_file)
    csv_writer.writerow([timestamp, temp, pressure, humidity, luminance, colour, aqi, uva_index, uvb_index, motion])
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
            temp = 0
            pressure = 0
            humidity = 0
            luminance = 'UNKNOWN'
            colour = 'UNKNOWN'
            aqi = 0
            motion = 'UNKNOWN'

            logging.debug('getting measurement')
            start_time = datetime.datetime.now()

            uva, uvb = uv_sensor.get_measurements()
            uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
            uv_indices = uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)
            uva_index, uvb_index, avg_uv_index = uv_indices

            end_time = datetime.datetime.now()

            store_measurement(temp, pressure, humidity, luminance, colour, aqi, uva, uvb, motion)

            display_measurement_time(start_time, end_time)

            img = Image.open("images/background.png").convert(oled.mode)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (128, 128)], fill="black")
            draw.text((0, 0), "UVA: {:05.01f}".format(uva_index), fill="white", font=rr_15)
            draw.text((0, 18), "UVB: {:05.01f}".format(uvb_index), fill="white", font=rr_15)
            oled.display(img)

            time.sleep(1)  # wait for one second
        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            sys.exit(0)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    main()
