from datetime import datetime
import logging
import requests
import time


import commands
import config_serivce
import data_files
import email_sender_service
import sensor_log_reader
import utils

logger = logging.getLogger('hc')

"""
Healthchech checks:
 - is app is running
 - when last measurement was
 - check when last photo was taken
if something wrong restart and send email
"""

attempts = 5
wait_time = 30
reasons = []


def capture_photo_is_older_than_5_minutes():
    filename = commands.get_last_photo_filename()
    return utils.is_file_older_than_5_minutes(filename)


def measurement_is_older_than_5_minutes():
    row = sensor_log_reader.get_last_measurement()
    timestamp = row['timestamp']
    return utils.is_timestamp_older_than_5_minutes(timestamp)


def healthcheck_test_runner():
    now = datetime.now().time()
    if now < datetime.now().time().replace(hour=0, minute=15, second=0, microsecond=0):
        logger.info("TOO EARLY. Healthcheck skipped.")
        return

    if datetime.now().time().replace(hour=3, minute=0, second=0, microsecond=0) < now < datetime.now().time().replace(
            hour=3, minute=15, second=0, microsecond=0):
        logger.info("JUST AFTER RESTART. Healthcheck skipped.")
        return

    try:
        passed = healthcheck_test()

        if not passed:
            for i in range(1, attempts + 1):
                logger.warning(
                    "health check failed {} time(s) ... waiting {} seconds before retry".format(i, wait_time))
                time.sleep(wait_time)
                passed = healthcheck_test()

                if passed:
                    break

        if passed:
            logger.info("PASSED")
        else:
            logger.error("FAILED ( {} )".format(reasons))
            send_email_on_fail("A {} attempts to pass healthcheck failed due to {}".format(attempts, str(reasons)))
            commands.reboot("Health check failed")

    except Exception as e:
        logger.error("ERROR ( {} )".format(e), exc_info=True)
        send_email_on_fail(str(e))


def healthcheck_test() -> bool:
    is_ok = True

    # check is ui is running
    ip = config_serivce.get_healthcheck_ip()
    response = requests.get(ip)
    if response.status_code != requests.codes.ok:
        is_ok = False
        reasons.append("WEB APP is not working")

    # check is pictures are taken
    if capture_photo_is_older_than_5_minutes():
        is_ok = False
        reasons.append("Capture photo is not working")

    # check is app is running
    if measurement_is_older_than_5_minutes():
        is_ok = False
        reasons.append("Getting measurement is not working")

    if not is_ok:
        logger.warning("FAILED ( {} )".format(response))

    return is_ok


def send_email_on_fail(problem: str):
    email_sender_service.send_error_log_email("healthcheck", problem)


if __name__ == '__main__':
    data_files.setup_logging()
    healthcheck_test_runner()
