import logging
import sys
import traceback

import pyaudio
import time
from math import log10
import audioop

import dom_utils
from common import data_files, loggy
from gateways import local_data_gateway

logger = logging.getLogger('app')
dom_utils.setup_logging('sound-sensor', False)
from datetime import datetime
# from timeit import default_timer as timer

EMPTY = ''

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())


def get_date_with_time_as_filename(name: str, file_type: str) -> str:
    dt = datetime.now()
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{file_type}"


def store_measurement(sensor_data: str, measurement: str):
    sensor_log_file = f"/home/ds/data/{get_date_with_time_as_filename(sensor_data, 'csv')}"
    try:
        with open(sensor_log_file, 'a+', newline=EMPTY, encoding='utf-8') as report_file:
            report_file.write(f'{measurement}\n')
    except IOError as measurement_exception:
        logger.error(f'Unable to save due to {measurement_exception}')
        print(measurement_exception)
        # add flag to indicate that there is a problem


def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


# TODO make it as method to be able to restart if failed
stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

noise_error = 0
noise_warn = 0
noise_caution = 0
noise_low = 0
avg10 = 0
prev_avg10 = 0
prev_prev_avg10 = 0
avg100 = 0
prev_avg100 = 0
prev_prev_avg100 = 0
avg600 = 0
prev_avg600 = 0
prev_prev_avg600 = 0
avgAll = 0
rms_min = 0
rms_max = 0
all = 0
counter = 0
last_results = []
list_size = 10 * 60 * 15
db_value = 0


def update_result(measurement):
    last_results.append(measurement)
    if len(last_results) > list_size:
        last_results.pop(0)


def update_averages():
    global avg10
    global prev_avg10
    global prev_prev_avg10
    global avg100
    global prev_avg100
    global prev_prev_avg100
    global avg600
    global prev_avg600
    global prev_prev_avg600

    last10 = last_results[-10:]
    total = 0
    for elem in last10:
        total += elem
    prev_prev_avg10 = prev_avg10
    prev_avg10 = avg10
    avg10 = total / 10

    last100 = last_results[-100:]
    for elem in last100:
        total += elem
    avg100 = total / 100

    prev_prev_avg100 = prev_avg600
    prev_avg600 = avg600

    last600 = last_results[-600:]
    for elem in last600:
        total += elem
    avg600 = total / 600
    prev_prev_avg600 = prev_avg600
    prev_avg600 = avg600


def get_diff_between(avg10, prev_avg10):
    return f'{(prev_avg10 - avg10):0.3f}'


def get_report():
    global counter
    global rms_min
    global rms_max
    global rms
    global noise_error
    global noise_warn
    global noise_caution
    global noise_low
    return {
        'timestamp': str(datetime.now()),
        'counter': counter,
        'rms': rms,
        'db' : db_value,
        'min_rms': rms_min,
        'max_rms': rms_max,
        'noise_detected': noise_low,
        'noise_detected_description': get_description_for_noise_level(noise_low),
        'noise_detected_percentage': dom_utils.percentage(noise_low, counter),
        'noise_caution': noise_caution,
        'noise_caution_description': get_description_for_noise_level(noise_caution),
        'noise_caution_percentage': dom_utils.percentage(noise_caution, counter),
        'noise_warn': noise_warn,
        'noise_warn_description': get_description_for_noise_level(noise_warn),
        'noise_warn_percentage': dom_utils.percentage(noise_warn, counter),
        'noise_error': noise_error,
        'noise_error_description': get_description_for_noise_level(noise_error),
        'noise_error_percentage': dom_utils.percentage(noise_low, counter),
        'avg10': avg10,
        'avg10_description': get_description_for_noise_level(avg10),
        'avg10_diff': get_diff_between(avg10, prev_avg10),
        'avg100': avg100,
        'avg100_description': get_description_for_noise_level(avg100),
        'avg100_diff': get_diff_between(avg100, prev_avg100),
        'avg600': avg600,
        'avg600_description': get_description_for_noise_level(avg600),
        'avg600_diff': get_diff_between(avg600, prev_avg600),
    }


def shutdown_all():
    logger.info('Shutting down ...')
    print('shutting down...')
    stream.stop_stream()
    print(f'Is stream stopped: {stream.is_stopped()}')
    stream.close()
    p.terminate()

def application():
    global counter
    global noise_low
    global noise_caution
    global noise_warn
    global noise_error
    global rms_min
    global rms_max
    global db_value

    logger.info('Warming up')
    logger.debug(f'initial value {rms}')
    time.sleep(1)
    logger.info('Starting application..')
    while stream.is_active():
        counter += 1

        current_value = rms
        logger.debug(f'RMS: {current_value}')

        db_value = 20 * log10(current_value)

        update_result(current_value)
        update_averages()
        if counter == 2:
            rms_min = current_value
            rms_max = current_value

        report_data = get_report()
        check_for_noise_alerts()
        if counter % 5 == 0:
            data_files.save_dict_data_to_file(report_data, 'sound-last-measurement')
        if counter % 25 == 0:
            logger.info(report_data)
        if counter > 3:
            if current_value > rms_max:
                rms_max = current_value
                logger.info(f'NEW MAX VALUE: {rms_max}')
            if rms_min > current_value:
                rms_min = current_value
                logger.debug(f'NEW MIN:{rms_min}')

        if counter % 250 == 0:
            logging.debug(
                f'CPU load: {stream.get_cpu_load()} Input latency: {stream.get_input_latency()} Output latency:  {stream.get_output_latency()}')

        if counter % 20 == 0:
            local_data_gateway.post_healthcheck_beat('denva2', 'sound')

        if counter % 100 == 0:
            data_files.store_measurement2(dom_utils.get_today_date_as_filename('sound-data', 'txt'),
                                          last_results[-100:])

def get_description_for_noise_level(value):
    if value > 0.61:
        return 'NOISE ALERT'
    elif value > 0.12:
        return 'NOISE WARNING'
    elif value > 0.012:
        return 'NOISE CAUTION'
    elif avg10 > 0.001:
        return 'NOISE DETECTED'
    return 'NO NOISE'

def check_for_noise_alerts():
    global noise_error, noise_warn, noise_caution, noise_low
    if avg10 > 0.61:
        noise_error += 1
    elif avg10 > 0.12:
        noise_warn += 1
    elif avg10 > 0.012:
        noise_caution += 1
    elif avg10 > 0.001:
        noise_low += 1


if __name__ == '__main__':
    try:
        application()
    except KeyboardInterrupt as keyboard_exception:
        shutdown_all()
        msg = f'Received request application to shut down.. goodbye. {keyboard_exception}'
        loggy.log_with_print(msg)
        sys.exit(0)
    except Exception as exception:
        shutdown_all()
        logger.fatal(exception, exc_info=True)
        print(f'error:{exception}')
        traceback.print_exc()
    except BaseException as disaster:
        shutdown_all()
        msg = f'Shit hit the fan and application died badly because {disaster}'
        logger.fatal(msg, exc_info=True)
        print(f'Error:{msg}')
        traceback.print_exc()
        logger.info('Application ended its life.')
