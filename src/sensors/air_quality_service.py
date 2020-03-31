import logging

from sgp30 import SGP30

from sensors import two_led_service

logger = logging.getLogger('app')

sgp30 = SGP30()

air_quality_led_status = 0
counter = 0


def get_eco2_measurement_as_string():
    return str(sgp30.get_air_quality().equivalent_co2)


def get_tvoc_measurement_as_string():
    return str(sgp30.get_air_quality().total_voc)


def crude_progress_bar():
    global air_quality_led_status
    global counter
    counter = counter + 1
    logger.warning('Waiting.. {}s.\n'.format(counter))
    air_quality_led_status = two_led_service.switch_led(air_quality_led_status)


def start_measurement():
    sgp30.start_measurement(crude_progress_bar)
