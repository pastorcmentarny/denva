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
import os
from collections import Counter
from timeit import default_timer as timer

import sys
from PIL import Image

deleted = 0


def get_all_photos_for() -> list:
    args = sys.argv[1:]
    path = "F:\\cctv\\{}\\{}\\{}\\".format(args[0], args[1], args[2])
    photos = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            photos.append(filename)
    return photos


def is_photo_mostly_black(file):
    global deleted
    if os.path.splitext(file)[-1].lower() != ".jpg":
        print('{} is not a photo. Ignore it')
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
        print(file + 'is too dark and need to be deleted.')
        try:
            os.remove(file)
            if os.path.exists(file):
                print('{} NOT deleted.'.format(file))
            else:
                print("{} deleted.".format(file))
                deleted += 1
        except Exception as e:
            print('unable to process {} file due to {}'.format(file, e))
    print(str(dark_pixels) + ' out of ' + str(total_pixels) + ' is dark. (' + str(too_dark) + '%)')


def check_is_pixel_too_dark(pixel) -> bool:
    dark = 6
    x, y, z = pixel
    return x <= dark and y <= dark and z <= dark


def main():
    global deleted
    all_photos = get_all_photos_for()
    for file in all_photos:
        start_time = timer()
        is_photo_mostly_black(file)
        end_time = timer()
        print(file + ' took ' + str(int((end_time - start_time) * 1000)) + 'milliseconds to process.')  # in ms

    print('We delete {} too dark pictures'.format(deleted))


if __name__ == '__main__':
    main()
