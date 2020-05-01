from bme280 import BME280
from common import commands

bme280 = BME280()

cpu_temps = []
factor = 0.8
temps = []


def get_temperature() -> int:
    global temps
    cpu_temp = commands.get_cpu_temp()
    # Smooth out with some averaging to decrease jitter
    temps = temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    return raw_temp - ((avg_cpu_temp - raw_temp) / factor)


def get_pressure():
    return bme280.get_pressure()


def get_humidity():
    return bme280.get_humidity()


# TODO provide sea level pressure
def get_altitude():
    return bme280.get_altitude()
