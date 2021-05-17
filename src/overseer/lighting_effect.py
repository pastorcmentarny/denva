import random
import time

PARADISE = 'paradise'
FLAME = 'flame'
YELLOW_GREEN = 'yellow_green'
MAGENTA = 'magenta'
CYAN = 'cyan'
YELLOW = 'yellow'
BROWN = 'brown'
BLACK = 'black'
WHITE = 'white'
PURPLE = 'purple'
BLUE = 'blue'
GREEN = 'green'
ORANGE = 'orange'
RED = 'red'
RED_RGB_COLOUR = [255, 0, 0]
ORANGE_RGB_COLOUR = [224, 64, 0]
GREEN_RGB_COLOUR = [0, 255, 0]
YELLOW_GREEN_RGB_COLOUR = [153, 204, 0]
BLUE_RGB_COLOUR = [0, 0, 255]
PURPLE_RGB_COLOUR = [75, 0, 130]
WHITE_RGB_COLOUR = [255, 255, 255]
BLACK_RGB_COLOUR = [1, 1, 1]
BROWN_RGB_COLOUR = [160, 96, 32]
YELLOW_RGB_COLOUR = [255, 255, 0]
CYAN_RGB_COLOUR = [0, 255, 255]
MAGENTA_RGB_COLOUR = [192, 0, 192]
FLAME_RGB_COLOUR = [242, 85, 44]
PARADISE_RGB_COLOUR = [144, 222, 227]
lighting_colors = [RED_RGB_COLOUR, ORANGE_RGB_COLOUR, GREEN_RGB_COLOUR, BLUE_RGB_COLOUR, PURPLE_RGB_COLOUR,
                   WHITE_RGB_COLOUR, BLACK_RGB_COLOUR, BROWN_RGB_COLOUR, YELLOW_RGB_COLOUR, CYAN_RGB_COLOUR,
                   MAGENTA_RGB_COLOUR, YELLOW_GREEN_RGB_COLOUR,
                   FLAME_RGB_COLOUR, PARADISE_RGB_COLOUR]


def update_to_next_line(line):
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
    return line


def lighting(mote):
    lighting_counter = random.randint(1, 3)
    for _ in range(0, lighting_counter):
        line = random.randint(1, 4)
        for led_index in range(0, 16):
            line = update_to_next_line(line)

            mote.set_pixel(line, led_index, 255, 255, 255, 1)
            mote.show()
            time.sleep(0.01)

        mote.clear()


def rainbow_lighting(mote):
    lighting_counter = random.randint(1, 3)
    for _ in range(0, lighting_counter):
        red, green, blue = lighting_colors[random.randint(0, len(lighting_colors) - 1)]
        line = random.randint(1, 4)
        for led_index in range(0, 16):
            line = update_to_next_line(line)

            mote.set_pixel(line, led_index, red, green, blue, 1)
            mote.show()
            time.sleep(0.01)
        repeat_count = random.randint(1, 4)

        for _ in range(1, repeat_count):
            min_brightness = random.randint(1, 3)
            for b in range(10, min_brightness, -1):
                update(b,mote)
            for b in range(min_brightness, 10, 1):
                update(b,mote)
        mote.clear()


def update(new_brightness: int,mote):
    mote.set_brightness(new_brightness / 10)
    mote.show()
    time.sleep(0.01)


if __name__ == '__main__':
    while True:
        rainbow_lighting()
