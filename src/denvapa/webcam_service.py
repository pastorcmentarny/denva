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
import os
import time
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer

import cv2

from common import dom_utils

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
logger = logging.getLogger('app')
step = 0.1

'''
if you see this, check is privacy setting for camera is set
"cv2.error: OpenCV(4.1.2) C:\\projects\\opencv-python\\opencv\\modules\\imgcodecs\\src\\loadsave.cpp:715: 
error: (-215:Assertion failed) !_img.empty() in function 'cv::imwrite'\n",
#TODO add detection permission for camera is ON 
'''


# FIXME
def capture_picture() -> str:
    logger.info('capturing a picture')
    try:
        start_time = timer()
        date_as_folders = dom_utils.get_date_as_folders_linux()
        path = Path("{}/{}".format("e:/sky/", date_as_folders))

        if not path.exists():
            print('creating')
            Path(path).mkdir(parents=True, exist_ok=True)

        file = dom_utils.get_date_with_time_as_filename("cctv", "jpg", datetime.now())

        photo_path = Path('{}/{}'.format(path, file))

        logger.info('using path {}'.format(photo_path))
        check, frame = webcam.read()
        cv2.imwrite(photo_path, frame)
        logger.info('saving image to file')
        while not os.path.exists(photo_path):
            time .sleep(step)
        logger.info('picture saved at {}'.format(photo_path))
        end_time = timer()
        total_time = str(int((end_time - start_time) * 1000))  # in ms
        logger.info('it took {} ms to generate picture.'.format(total_time))
        return photo_path
    except Exception as e:
        logger.warning('Unable to capture picture due to {}'.format(e), exc_info=True)
        # TODO email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(e))
    return ""
