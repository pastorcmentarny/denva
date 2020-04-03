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
from random import randint

import unicornhathd

print("""Idle mode:""")

unicornhathd.rotation(90)
unicornhathd.brightness(0.6)

green_rgb = [
    [154, 173, 154], [0, 255, 0], [0, 235, 0], [0, 220, 0],
    [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0],
    [154, 173, 154], [0, 145, 0], [0, 125, 0], [0, 100, 0],
    [0, 80, 0], [0, 60, 0], [0, 40, 0], [0, 0, 0]
]

orange_rgb = [
    [154, 173, 154], [255, 110, 0], [235, 101, 0], [220, 94, 0],
    [185, 80, 0], [165, 70, 0], [128, 55, 0], [0, 0, 0],
    [154, 173, 154], [145, 62, 0], [125, 53, 0], [100, 43, 0],
    [80, 34, 0], [60, 26, 0], [40, 17, 0], [0, 0, 0]
]

clock = 0

blue_pilled_population = [[randint(0, 15), 15,'orange'],[randint(0, 15), 15,'green']]


def generate_person_of_color(person_color:str):
    if person_color is 'orange':
        shape = orange_rgb
    elif person_color is 'green':
        shape = green_rgb
    else:
        shape = []
    y = person[1]
    for rgb in shape:
        if (y <= 15) and (y >= 0):
            unicornhathd.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
        y += 1

colors = ['orange','green']
def get_random_color() -> str:
    result = randint(0,1)
    return colors[result]


try:
    while True:
        for person in blue_pilled_population:
            person_color = person[2]
            generate_person_of_color(person_color)
            person[1] -= 1
        unicornhathd.set_pixel(0, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(15, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(0, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.set_pixel(15, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.show()
        time.sleep(0.1)
        clock += 1

        if clock % 5 == 0:
            blue_pilled_population.append([randint(0, 15), 15,get_random_color()])
        if clock % 7 == 0:
            blue_pilled_population.append([randint(0, 15), 15,get_random_color()])

        while len(blue_pilled_population) > 100:
            blue_pilled_population.pop(0)

except KeyboardInterrupt:
    unicornhathd.off()
