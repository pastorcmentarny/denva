import logging
import requests

import commands
import email_sender_service
import sensor_log_reader
import utils

logger = logging.getLogger('healthCheck')


# */5 * * * * sudo python3 /home/pi/denva-master/src/healthcheck.py

# check is app is running
# check when last measurement was
# check when last photo was taken
# if something wrong restart and send email


def capture_photo_is_older_than_5_minutes():
    filename = commands.get_last_photo_filename()
    return utils.is_file_older_than_5_minutes(filename)


def measurement_is_older_than_5_minutes():
    row = sensor_log_reader.get_last_measurement()
    timestamp = row['timestamp']
    return utils.is_timestamp_older_than_5_minutes(timestamp)


def healthcheck_test():
    ok = True
    reasons = []

    try:
        # check is ui is running
        response = requests.get('http://192.168.0.3:5000/hc')
        if response.status_code != requests.codes.ok:
            ok = False
            reasons.append("WEB APP is not working")

        # check is pictures are taken
        if capture_photo_is_older_than_5_minutes():
            ok = False
            reasons.append("Capture photo is not working")

        # check is app is running
        if measurement_is_older_than_5_minutes():
            ok = False
            reasons.append("Getting measurement is not working")

        if ok:
            logger.info("PASSED")
        else:
            logger.warning("FAILED ( {} )".format(response))
            send_email_on_fail(str(reasons))
    except Exception as e:
        logger.error("ERROR ( {} )".format(e), exc_info=True)
        send_email_on_fail(str(e))

def send_email_on_fail(problem: str):
    email_sender_service.send_error_log_email("healthcheck", problem)


if __name__ == '__main__':
    healthcheck_test()
