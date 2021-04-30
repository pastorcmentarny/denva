import random
import time

from mote import Mote

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()
mote.set_brightness(0.2)
BLACK_RGB_COLOR = [0, 0, 0, 0.1]
BROWN_RGB_COLOUR = [160, 96, 32]
RED_RGB_COLOUR = [255, 0, 0, 0.3]
ORANGE_RGB_COLOUR = [127, 63, 0, 0.5]
YELLOW_RGB_COLOUR = [255, 255, 0, 0.8]
WHITE_RGB_COLOUR = [255, 255, 255, 1]

RED_VALUE = 0
GREEN_VALUE = 1
BLUE_VALUE = 2
BRIGHTNESS = 3

WAIT_TIME = 0.2


def transform():
    for r in range(0, 255):
        change_to(int(r), 0, 0, 0.2)

    for r in range(255, 160, -1):
        change_to(int(r), 0, 0, 0.2)

    for r in range(160, 255):
        change_to(int(r), 0, 0, 0.2)

    for r in range(255, 32, -1):
        change_to(int(r), 0, 0, 0.2)

    repeat = random.randint(1, 10)
    for _ in range(0, repeat):
        for _ in range(32, 128):
            change_to(_, int(_ / 2), 0, 0.3)
        for _ in range(128, 32):
            change_to(_, int(_ / 2), 0, 0.3)

    repeat = random.randint(1, 20)
    for _ in range(0, repeat):
        for r in range(64, 224):
            change_to(int(r), int(r * 2 / 3), 0, 0.1)

        for r in range(224, 64, -1):
            change_to(int(r), int(r * 2 / 3), 0, 0.1)


def change_to(red: int, green: int, blue: int, brightness=0.2):
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, red, green, blue, brightness)
    mote.show()


def lighting():
    lighting_counter = random.randint(1, 3)
    for _ in range(0, lighting_counter):
        line = random.randint(1, 4)
        for led_index in range(0, 16):
            if line == 1:
                direction = random.randint(1, 2)
                if direction == 2:
                    line += 1
            elif line == 4:
                direction = random.randint(1, 2)
                if direction == 1:
                    line -= 1
            else:
                direction = random.randint(1, 3)
                if direction == 1:
                    line -= 1
                else:
                    line += 1

            mote.set_pixel(line, led_index, 255, 255, 255, 1)
            mote.show()
            time.sleep(0.01)

        mote.clear()


def fire_effect_with_lighting():
    while True:
        for _ in range(1, 3):
            transform()

        probability = random.randint(1, 100)
        if probability > 88:
            for _ in range(1, probability):
                lighting()
        elif probability > 68:
            lighting()


if __name__ == '__main__':
    fire_effect_with_lighting()
