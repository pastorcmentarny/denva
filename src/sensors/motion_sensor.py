#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging
import time

from icm20948 import ICM20948

from gateways import local_data_gateway

logger = logging.getLogger('app')
points = []


def setup():
    return ICM20948()


imu = setup()

sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()
mx, my, mz = imu.read_magnetometer_data()
print(
    f'initial data from ICM20948 sx:${sx}, sy:${sy}, sz:${sz}, sgx:${sgx}, sgy:${sgy}, sgz:${sgz}, mx:${mx}, my:${my}, mz:${mz})')


def reset():
    global imu
    time.sleep(5)
    try:
        imu = ICM20948()
    except Exception as exception:
        print(f'Unable to restart ICM20948 due to {exception}')
        raise exception


def sample():
    for i in range(51):
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz

        v = ay  # Change this axis depending on orientation of breakout

        v *= 8

        points.append(v)
        if len(points) > 50:
            points.pop(0)

        time.sleep(0.01)


def get_measurement() -> dict:
    try:
        current_mx, current_my, current_mz = imu.read_magnetometer_data()
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz
        return {
            'ax': ax, 'ay': ay, 'az': az,
            'gx': gx, 'gy': gy, 'gz': gz,
            'mx': current_mx, 'my': current_my, 'mz': current_mz
        }
    except Exception as motion_exception:
        local_data_gateway.post_metrics_update('motion', 'errors')
        logger.error(
            f'Unable to read data from icm20948 (motion sensor) sensor due to {type(motion_exception).__name__} throws : {motion_exception}')
        reset()
        raise motion_exception


def get_motion() -> int:
    try:
        sample()
        value = 0
        for i in range(1, len(points)):
            value += abs(points[i] - points[i - 1])
        return value
    except Exception as motion_exception:
        logger.error(
            f'Unable to restart ICM20948 due to {type(motion_exception).__name__} throws : {motion_exception}',
            exc_info=True)
        reset()
        return 0
