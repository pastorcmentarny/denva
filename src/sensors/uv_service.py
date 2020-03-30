import smbus
import veml6075

bus = smbus.SMBus(1)

# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')


def get_measurements():
    uva, uvb = uv_sensor.get_measurements()
    uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
    return uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)