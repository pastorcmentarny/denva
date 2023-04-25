import logging
import time
from gateways import local_data_gateway
from as7262 import AS7262

logger = logging.getLogger('app')


def get_sensor_instance():
    sensor_instance = AS7262()
    sensor_instance.set_gain(64)
    sensor_instance.set_integration_time(17.857)
    sensor_instance.set_measurement_mode(2)
    sensor_instance.set_illumination_led(0)
    return sensor_instance


as7262 = get_sensor_instance()


def get_measurement():
    global as7262
    try:
        values = as7262.get_calibrated_values()

        return {
            'red': values.red,
            'orange': values.orange,
            'yellow': values.yellow,
            'green': values.green,
            'blue': values.blue,
            'violet': values.violet
        }
    except Exception as spectrometer_exception:
        logger.error(
            f'Unable to restart ICM20948 due to {type(spectrometer_exception).__name__} throws : {spectrometer_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('spectrometer', 'errors')
        print(f'It was a problem with spectrometer sensor caused by {spectrometer_exception}.')
        time.sleep(1)
        as7262 = get_sensor_instance()
        print('Sensor as7262 restarted.')
        as7262.set_illumination_led(0)
        return 0, 0, 0, 0, 0, 0
