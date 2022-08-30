import dom_utils
import logging.config
from datetime import datetime
from timeit import default_timer as timer
from common import commands, data_files
from denva import cl_display, denva_sensors_service
from gateways import local_data_gateway
from sensors import environment_service, gps_sensor, co2_sensor, air_quality_service, two_led_service

logger = logging.getLogger('app')


def get_data_from_measurement() -> dict:
    environment = environment_service.get_measurement()
    eco2, tvoc = air_quality_service.get_all_measurements()
    red, green, blue = two_led_service.get_measurement()
    colour = dom_utils.to_hex(red, green, blue)
    gps_data = gps_sensor.get_measurement()
    co2_data = co2_sensor.get_measurement()

    return {
        "temp": environment['temp'], "pressure": environment['pressure'], "humidity": environment['humidity'],
        "gas_resistance": "{:.2f}".format(environment['gas_resistance']),
        "colour": colour,
        "r": red, "g": green, "b": blue,
        "eco2": eco2, "tvoc": tvoc,
        'gps_latitude': gps_data['latitude'], 'gps_longitude': gps_data['longitude'],
        'gps_altitude': gps_data['altitude'],
        'gps_lat_dir': gps_data['lat_dir'], 'gps_lon_dir': gps_data['lon_dir'], 'gps_geo_sep': gps_data['geo_sep'],
        'gps_num_sats': gps_data['num_sats'], 'gps_qual': gps_data['gps_qual'],
        'gps_speed_over_ground': gps_data['speed_over_ground'], 'gps_mode_fix_type': gps_data['mode_fix_type'],
        'gps_pdop': gps_data['pdop'], 'gps_hdop': gps_data['hdop'], 'gps_vdop': gps_data['vdop'],
        "co2": co2_data[0],
        "co2_temperature": co2_data[1],
        "relative_humidity": co2_data[2]
    }


def get_measurement_from_all_sensors(measurement_counter, start_time):
    data = get_data_from_measurement()
    data['cpu_temp'] = commands.get_cpu_temp()
    end_time = timer()
    measurement_time = int((end_time - start_time) * 1000)  # in ms
    logger.info('Measurement no. {} took {} milliseconds to measure it.'
                .format(measurement_counter, measurement_time))
    data['measurement_counter'] = measurement_counter
    data['measurement_time'] = str(measurement_time)
    data_files.store_measurement(data, denva_sensors_service.get_sensor_log_file())
    cl_display.print_measurement(data)
    local_data_gateway.post_denva_measurement(data)
    return measurement_time
