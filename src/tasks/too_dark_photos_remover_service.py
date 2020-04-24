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
from collections import Counter
from timeit import default_timer as timer

import sys
from PIL import Image

from utils import data_files

logger = logging.getLogger('server')
deleted = 0
ignored = 0
errors = 0


def get_all_photos_for() -> list:
    args = sys.argv[1:]
    path = "F:\\cctv\\{}\\{}\\{}\\".format(args[0], args[1], args[2])
    logger.info("Generating list of files to process for {}.{}'{}".format(args[2], args[1], args[0]))
    photos = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            photos.append(filename)
    logger.info("Collected {} file(s) to process.".format(len(photos)))
    return photos


def is_photo_mostly_black(file):
    global deleted
    global ignored
    global errors
    if os.path.splitext(file)[-1].lower() != ".jpg":
        logger.warning('{} is not a photo. Ignore it.')
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
                logger.warning('{} NOT deleted.'.format(file))
            else:
                logger.info("{} deleted.".format(file))
                deleted += 1
        except Exception as e:
            logger.error('Unable to process {} file due to {}'.format(file, e))
            errors += 1
    logger.info(str(dark_pixels) + ' out of ' + str(total_pixels) + ' is dark. (' + str(too_dark) + '%)')


def check_is_pixel_too_dark(pixel) -> bool:
    dark = 6
    x, y, z = pixel
    return x <= dark and y <= dark and z <= dark


def setup():
    data_files.setup_logging()


def main():
    global deleted
    global ignored
    global errors
    logger.info('Starting a server app')
    all_photos = get_all_photos_for()

    all_start_time = timer()

    for file in all_photos:
        start_time = timer()
        is_photo_mostly_black(file)
        end_time = timer()
        logger.info(file + ' took ' + str(int((end_time - start_time) * 1000)) + 'milliseconds to process.')  # in ms

    all_end_time = timer()
    total_time = int((all_end_time - all_start_time) * 1000)
    logger.info('it took {} milliseconds to process all files.'.format(total_time))  # in ms

    logger.info(
        'DONE!'
        '\nWe deleted {} too dark pictures.\nWe ignored {} non-photo pictures.\nWe got {} errors while processing.\n'
        'Bye!'.format(deleted, ignored, errors))


if __name__ == '__main__':
    setup()
    main()
