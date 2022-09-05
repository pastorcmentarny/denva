import dom_utils
import logging.config

from timeit import default_timer as timer
from common import commands, data_files
from denva import cl_display, denva_sensors_service
from gateways import local_data_gateway
from sensors import environment_service, gps_sensor, co2_sensor, air_quality_service, two_led_service
import config

logger = logging.getLogger('app')


def get_data_from_measurement() -> dict:
    environment = environment_service.get_measurement()
    eco2, tvoc = air_quality_service.get_all_measurements()
    red, green, blue = two_led_service.get_measurement()
    colour = dom_utils.to_hex(red, green, blue)
    gps_data = gps_sensor.get_measurement()
    co2_data = co2_sensor.get_measurement()

    return {
        config.FIELD_TEMPERATURE: environment[config.FIELD_TEMPERATURE],
        config.FIELD_PRESSURE: environment[config.FIELD_PRESSURE],
        config.FIELD_HUMIDITY: environment[config.FIELD_HUMIDITY],
        config.FIELD_GAS_RESISTANCE: "{:.2f}".format(environment[config.FIELD_GAS_RESISTANCE]),
        config.FIELD_COLOUR: colour,
        config.FIELD_RED: red, config.FIELD_GREEN: green, config.FIELD_BLUE: blue,
        config.FIELD_ECO2: eco2, config.FIELD_TVOC: tvoc,
        config.FIELD_GPS_LATITUDE: gps_data['latitude'], config.FIELD_GPS_LONGITUDE: gps_data['longitude'],
        config.FIELD_GPS_ALTITUDE: gps_data['altitude'],
        config.FIELD_GPS_LAT_DIR: gps_data['lat_dir'], config.FIELD_GPS_LON_DIR: gps_data['lon_dir'],
        config.FIELD_GPS_GEO_SEP: gps_data['geo_sep'], config.FIELD_GPS_NUM_SATS: gps_data['num_sats'],
        config.FIELD_GPS_QUAL: gps_data['gps_qual'], config.FIELD_GPS_SPEED_OVER_GROUND: gps_data['speed_over_ground'],
        config.FIELD_GPS_MODE_FIX_TYPE: gps_data['mode_fix_type'], config.FIELD_GPS_PDOP: gps_data['pdop'],
        config.FIELD_GPS_HDOP: gps_data['hdop'], config.FIELD_GPS_VDOP: gps_data['vdop'],
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
    local_data_gateway.post_denva_measurement(data)
    return measurement_time
