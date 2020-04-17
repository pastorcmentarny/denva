import logging
import os
from datetime import datetime
from timeit import default_timer as timer

import cv2
import time

import utils

webcam = cv2.VideoCapture(0)
logger = logging.getLogger('server')
step = 0.1


def capture_picture() -> str:
    logger.info('capturing a picture')
    try:
        start_time = timer()
        date_path = datetime.now().strftime("%Y\\%m\\%d")
        path = "F:\\cctv\\{}\\".format(date_path)
        if not os.path.isdir(path):
            logger.info('creating folder for {}'.format(path))
            os.makedirs(path)
        date = utils.get_timestamp_file()
        photo_path = '{}\\{}.jpg'.format(path, date)
        logger.info(photo_path)
        check, frame = webcam.read()
        cv2.imwrite(photo_path, frame)
        logger.info('saving image to file')
        while not os.path.exists(photo_path):
            time.sleep(step)
        logger.info('picture saved at {}'.format(photo_path))
        end_time = timer()
        total_time = str(int((end_time - start_time) * 1000))  # in ms
        logger.info('it took {} milliseconds to measure it.'.format(total_time))
        return photo_path
    except Exception as e:
        logger.warning('Something went badly wrong\n{}'.format(e), exc_info=True)
        # TODO email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(e))
    logger.warning('No path returned due to previous error.')
    return ""
