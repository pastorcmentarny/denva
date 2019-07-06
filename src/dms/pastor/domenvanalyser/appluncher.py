import datetime
import logging
import sys
import time

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='denva-log.txt')


def display_measurement_time(start_time, end_time):
    result = end_time.microsecond - start_time.microsecond
    logging.debug('it took ' + str(result) + ' microseconds to measure it.')


def main():
    while True:
        try:
            temp = 0
            pressure = 0
            humidity = 0
            luminance = 'UNKNOWN'
            colour = 'UNKNOWN'
            aqi = 0
            uva = 0
            uvb = 0
            motion = 'UNKNOWN'
            logging.debug('getting measurement')
            start_time = datetime.datetime.now()
            measurement = 'temp: {} pressure: {} humidity: {} luminace: {} colour: {} AQI: {} UVA: {} UVB: {} motion: {}'.format(
                temp, pressure, humidity, luminance, colour, aqi, uva, uvb, motion)
            logging.info(measurement)
            print(measurement)
            end_time = datetime.datetime.now()

            display_measurement_time(start_time, end_time)

            time.sleep(1)  # wait for one second
        except KeyboardInterrupt:
            print('request application shut down.. goodbye!')
            sys.exit(0)


if __name__ == '__main__':
    print('Starting application ... \n Press Ctrl+C to shutdown')
    main()
