import logging
import random
logger = logging.getLogger('app')


def in_the_warp(unicornhathd,clock,cycle):

    cycle += 1
    logger.info('Spacedate: {}. Currently, we are in the warp..'.format(cycle))

    star_count = 25
    star_speed = 0.01
    stars = []

    for i in range(0, star_count):
        stars.append((random.uniform(4, 11), random.uniform(4, 11), 0))

    running = True
    while running:
        unicornhathd.clear()
        clock += 1
        for i in range(0, star_count):
            stars[i] = (
                stars[i][0] + ((stars[i][0] - 8.1) * star_speed),
                stars[i][1] + ((stars[i][1] - 8.1) * star_speed),
                stars[i][2] + star_speed * 50)

            if stars[i][0] < 0 or stars[i][1] < 0 or stars[i][0] > 16 or stars[i][1] > 16:
                stars[i] = (random.uniform(4, 11), random.uniform(4, 11), 0)

            v = stars[i][2]

            unicornhathd.set_pixel(stars[i][0], stars[i][1], v, v, v)

        unicornhathd.show()

        if clock % 50 == 0:
            star_speed += 0.001
        if clock % 4000 == 0:
            running = False