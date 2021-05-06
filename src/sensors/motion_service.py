#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import logging
import time

from icm20948 import ICM20948

import config_service

logger = logging.getLogger('app')
points = []

imu = ICM20948()
sx, sy, sz, sgx, sgy, sgz = imu.read_accelerometer_gyro_data()
mx, my, mz = imu.read_magnetometer_data()
logger.info(
    f'initial data from ICM20948 sx:${sx}, sy:${sy}, sz:${sz}, sgx:${sgx}, sgy:${sgy}, sgz:${sgz}, mx:${mx}, my:${my}, mz:${mz})')


def reset():
    global imu
    logger.warning("Resetting motion sensor ICM20948")
    logger.info("Waiting 5 seconds..")
    time.sleep(5)
    logger.info("Resetting ICM20948 sensor")
    try:
        imu = ICM20948()
        logger.info("Reset complete")
    except Exception as exception:
        logger.error('Unable to restart ICM20948 due to {}'.format(exception), exc_info=True)
        raise Exception(exception)

    test_mx, test_my, test_mz = imu.read_magnetometer_data()
    test_ax, test_ay, test_az, test_gx, test_gy, test_gz = imu.read_accelerometer_gyro_data()
    logger.info(
        f'initial data from ICM20948 ax:${test_ax}, ay:${test_ay}, az:${test_az}, gx:${test_gx}, sgy:${test_gy}, sgz:${test_gz}, mx:${test_mx}, my:${test_my}, mz:${test_mz})')


def sample():
    for i in range(51):
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz

        v = ay  # Change this axis depending on orientation of breakout

        v *= (config_service.get_sensitivity())

        points.append(v)
        if len(points) > 50:
            points.pop(0)

        time.sleep(0.01)


def get_current_motion_difference() -> dict:
    try:
        mx, my, mz = imu.read_magnetometer_data()
        ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

        ax -= sx
        ay -= sy
        az -= sz
        return {
            'ax': ax, 'ay': ay, 'az': az,
            'gx': gx, 'gy': gy, 'gz': gz,
            'mx': mx, 'my': my, 'mz': mz
        }
    except Exception as exception:
        logger.warning(f"Unable to read data due to ${exception}")
        reset()


def get_motion() -> int:
    try:
        sample()
        value = 0
        for i in range(1, len(points)):
            value += abs(points[i] - points[i - 1])
        return value
    except Exception as exception:
        logger.info('Exception occurred while getting data', exception)
        reset()
        return 0
