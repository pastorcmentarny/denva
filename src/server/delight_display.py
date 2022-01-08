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

import time
import unicornhathd


def show(pixels, speed: float = 0.5):
    for pixel in pixels:
        unicornhathd.set_pixel(pixel[0], pixel[1], pixel[2], pixel[3], pixel[4])
    unicornhathd.show()
    time.sleep(speed)


# TODO replace with clear command
def reset_screen():
    for x in range(0, 16):
        for y in range(0, 16):
            unicornhathd.set_pixel(x, y, 0, 0, 0)
    unicornhathd.show()
