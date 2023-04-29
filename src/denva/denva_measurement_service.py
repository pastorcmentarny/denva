import dom_utils
import logging.config

from timeit import default_timer as timer
from common import commands, data_files
from denva import cl_display, denva_sensors_service, denva_service
from gateways import local_data_gateway
from sensors import environment_sensor, co2_sensor, air_quality_sensor, two_led_service, uv_sensor
import config

logger = logging.getLogger('app')


def get_data_from_measurement() -> dict:

    environment = environment_sensor.get_measurement()
    eco2, tvoc = air_quality_sensor.get_all_measurements()
    red, green, blue = two_led_service.get_measurement()
    colour = dom_utils.to_hex(red, green, blue)
    co2_data = co2_sensor.get_measurement()
    uv_data = uv_sensor.get_measurement()


    return {
        config.FIELD_TEMPERATURE: environment[config.FIELD_TEMPERATURE],
        config.FIELD_PRESSURE: environment[config.FIELD_PRESSURE],
        config.FIELD_HUMIDITY: environment[config.FIELD_HUMIDITY],
        config.FIELD_GAS_RESISTANCE: "{:.2f}".format(environment[config.FIELD_GAS_RESISTANCE]),
        config.FIELD_COLOUR: colour,
        config.FIELD_RED: red, config.FIELD_GREEN: green, config.FIELD_BLUE: blue,
        config.FIELD_ECO2: eco2, config.FIELD_TVOC: tvoc,
        config.FIELD_CO2: co2_data[0], config.FIELD_CO2_TEMPERATURE: co2_data[1],
        config.FIELD_RELATIVE_HUMIDITY: co2_data[2]
    }


def get_measurement_from_all_sensors(measurement_counter, start_time):
    data = get_data_from_measurement()
    data[config.FIELD_CPU_TEMP] = commands.get_cpu_temp()
    end_time = timer()
    measurement_time = int((end_time - start_time) * 1000)  # in ms
    logger.info('Measurement no. {} took {} milliseconds to measure it.'
                .format(measurement_counter, measurement_time))
    data[config.FIELD_MEASUREMENT_COUNTER] = measurement_counter
    data[config.FIELD_MEASUREMENT_TIME] = str(measurement_time)
    data_files.store_measurement(data, denva_sensors_service.get_sensor_log_file())
    cl_display.print_measurement(data)
    warnings = denva_service.get_current_warnings()
    data_files.save_warnings(warnings)
    local_data_gateway.post_denva_measurement(data)
    return measurement_time
