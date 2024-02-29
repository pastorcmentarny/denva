import logging
import random
from server import display

logger = logging.getLogger('app')


def in_the_warp():
    clock = 0

    star_count = 25
    star_speed = 0.01
    stars = []

    for i in range(0, star_count):
        stars.append((random.uniform(4, 11), random.uniform(4, 11), 0))

    for idx in range(0, 4000):
        display.unicornhathd.clear()
        clock += 1
        for i in range(0, star_count):
            stars[i] = (
                stars[i][0] + ((stars[i][0] - 8.1) * star_speed),
                stars[i][1] + ((stars[i][1] - 8.1) * star_speed),
                stars[i][2] + star_speed * 50)

            if stars[i][0] < 0 or stars[i][1] < 0 or stars[i][0] > 16 or stars[i][1] > 16:
                stars[i] = (random.uniform(4, 11), random.uniform(4, 11), 0)

            v = stars[i][2]

            display.unicornhathd.set_pixel(stars[i][0], stars[i][1], v, v, v)

        display.unicornhathd.show()

        if clock % 50 == 0:
            star_speed += 0.001
