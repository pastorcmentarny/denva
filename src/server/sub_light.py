import logging
import time
from random import randint
from server import display

logger = logging.getLogger('app')

BLUE = 'blue'
GREY = 'grey'
GREEN = 'green'
ORANGE = 'orange'
PURPLE = 'purple'
RED = 'red'
YELLOW = 'yellow'

grey_rgb = [
    [154, 173, 154], [255, 255, 255], [235, 235, 235], [220, 220, 220],
    [185, 185, 185], [165, 165, 165], [128, 128, 128], [0, 0, 0]
]

blue_rgb = [
    [154, 173, 154], [0, 0, 255], [0, 0, 235], [0, 0, 220],
    [0, 0, 185], [0, 0, 165], [0, 0, 128], [0, 0, 0]
]

purple_rgb = [
    [154, 173, 154], [160, 32, 240], [144, 30, 220], [128, 28, 200],
    [112, 26, 180], [96, 24, 160], [80, 16, 120], [0, 0, 0]
]

green_rgb = [
    [154, 173, 154], [0, 255, 0], [0, 235, 0], [0, 220, 0],
    [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0]
]

red_rgb = [
    [154, 173, 154], [255, 0, 0], [235, 0, 0], [220, 0, 0],
    [185, 0, 0], [165, 0, 0], [128, 0, 0], [0, 0, 0]
]

yellow_rgb = [
    [154, 173, 154], [255, 224, 32], [235, 202, 30], [220, 188, 28],
    [185, 153, 26], [165, 133, 24], [128, 96, 22], [0, 0, 0]
]

orange_rgb = [
    [154, 173, 154], [255, 110, 0], [235, 101, 0], [220, 94, 0],
    [185, 80, 0], [165, 70, 0], [128, 55, 0], [0, 0, 0]
]

colors = [ORANGE, GREEN, GREY, BLUE, PURPLE, RED, YELLOW]  # change generate function too


def get_population() -> list:
    people = []
    for color in colors:
        people.append([randint(0, 15), 15, color])
    return people


blue_pilled_population = get_population()


def get_random_color() -> str:
    result = randint(0, len(colors) - 1)
    return colors[result]


def generate_person_of_color(person_color: str, person: list):
    if person_color is ORANGE:
        shape = orange_rgb
    elif person_color is GREEN:
        shape = green_rgb
    elif person_color is GREY:
        shape = grey_rgb
    elif person_color is BLUE:
        shape = blue_rgb
    elif person_color is PURPLE:
        shape = purple_rgb
    elif person_color is RED:
        shape = red_rgb
    elif person_color is YELLOW:
        shape = yellow_rgb
    else:
        shape = []

    y = person[1]
    for rgb in shape:
        if (y < 15) and (y > 0):
            display.unicornhathd.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
        y += 1


def sub_light_travel():
    clock = 0

    running = True
    while running:
        for person in blue_pilled_population:
            person_color = person[2]
            generate_person_of_color(person_color, person)
            person[1] -= 1
        display.unicornhathd.set_pixel(0, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        display.unicornhathd.set_pixel(15, 0, randint(0, 255), randint(0, 255), randint(0, 255))
        display.unicornhathd.set_pixel(0, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        display.unicornhathd.set_pixel(15, 15, randint(0, 255), randint(0, 255), randint(0, 255))
        display.unicornhathd.show()
        time.sleep(0.075)
        clock += 1

        if clock % 5 == 0:
            blue_pilled_population.append([randint(0, 15), 15, get_random_color()])
        if clock % 7 == 0:
            blue_pilled_population.append([randint(0, 15), 15, get_random_color()])

        while len(blue_pilled_population) > 100:
            blue_pilled_population.pop(0)

        if clock % 125 == 0:
            running = False
