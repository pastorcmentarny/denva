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
import datetime
import logging
import os
from collections import Counter
from pathlib import Path
from timeit import default_timer as timer

from PIL import Image

import config

logger = logging.getLogger('server')
deleted = 0
ignored = 0
errors = 0


def get_all_photos_for(year: str, month: str, day: str) -> list:
    path = str(Path(f"{config.PI_DATA_PATH}{year}/{month}/{day}/"))
    logger.info(f"Generating list of files to process for {day}.{month}'{year}")
    photos = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            photos.append(path + filename)
    logger.info(f"Collected {len(photos)} file(s) to process.")
    return photos


def remove_if_too_dark(file) -> bool:
    if os.path.splitext(file)[-1].lower() != ".jpg":
        logger.warning('{} is not a photo. Ignore it.')
        return True

    im = Image.open(file)  # Can be many different formats.
    total_pixels = im.width * im.height
    pix = im.load()

    counter = []

    for x in range(0, im.width):
        for y in range(0, im.height):
            counter.append(pix[x, y])

    result = Counter(counter)
    dark_pixels = 0
    for d in result.items():
        if check_is_pixel_too_dark(d[0]):
            dark_pixels += d[1]
    too_dark = dark_pixels / total_pixels * 100
    if too_dark > 95:
        logger.info(file + 'is too dark and need to be deleted.')
        try:
            os.remove(file)
            if os.path.exists(file):
                logger.warning(f'{file} NOT deleted.')
                return True
            else:
                logger.info(f"{file} deleted.")
                return True
        except Exception as e:
            logger.error(f'Unable to process {file} file due to {e}')
            return True
    else:
        return False


def is_photo_mostly_black(file, with_summary: bool = True):
    global deleted
    global ignored
    global errors
    if os.path.splitext(file)[-1].lower() != ".jpg":
        logger.warning(f'{file} is not a photo. Ignore it.')
        ignored += 1
        return

    im = Image.open(file)  # Can be many different formats.
    total_pixels = im.width * im.height
    pix = im.load()

    counter = []

    for x in range(0, im.width):
        for y in range(0, im.height):
            counter.append(pix[x, y])

    result = Counter(counter)
    dark_pixels = 0
    for d in result.items():
        if check_is_pixel_too_dark(d[0]):
            dark_pixels += d[1]
    too_dark = dark_pixels / total_pixels * 100
    if too_dark > 95:
        logger.info(file + 'is too dark and need to be deleted.')
        try:
            os.remove(file)
            if os.path.exists(file):
                logger.warning(f'{file} NOT deleted.')
            else:
                logger.info(f"{file} deleted.")
                deleted += 1
        except Exception as e:
            logger.error(f'Unable to process {file} file due to {e}')
            errors += 1
    if with_summary:
        logger.info(str(dark_pixels) + ' out of ' + str(total_pixels) + ' is dark. (' + str(too_dark) + '%)')


def check_is_pixel_too_dark(pixel) -> bool:
    dark = 6
    x, y, z = pixel
    return x <= dark and y <= dark and z <= dark


def setup():
    logging.basicConfig(level=logging.DEBUG)
    logging.captureWarnings(True)
    logging.debug('Running test logging')


def process_for_yesterday():
    yesterday = datetime.datetime.now() + datetime.timedelta(days=-1)
    process_for_date(str(yesterday.year), f'{yesterday.month:02d}', f'{yesterday.day:02d}')


def process_for_date(year: str, month: str, day: str):
    global deleted
    global ignored
    global errors
    logger.info('Starting a server app')
    all_photos = get_all_photos_for(year, month, day)

    all_start_time = timer()

    for file in all_photos:
        start_time = timer()
        is_photo_mostly_black(file)
        end_time = timer()
        logger.info(file + ' took ' + str(int((end_time - start_time) * 1000)) + 'ms to process.')  # in ms

    all_end_time = timer()
    total_time = int((all_end_time - all_start_time) * 1000)
    logger.info(f'it took {total_time} ms to process all files.')  # in ms

    logger.info(
        'DONE!'
        '\nWe deleted {} too dark pictures.\nWe ignored {} non-photo pictures.\nWe got {} errors while processing.\n'
        'Bye!'.format(deleted, ignored, errors))


if __name__ == '__main__':
    setup()
    """
    args = sys.argv[1:]
    process_for_date(args[0], args[1], args[2])
    """
    process_for_yesterday()
