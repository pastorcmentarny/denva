import random
import time

from mote import Mote

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()


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


def orange_lighting():
    pixels = []
    lighting_counter = random.randint(1, 3)
    for _ in range(0, lighting_counter):
        line = random.randint(1, 4)
        for led_index in range(0, 16):
            line = update_to_next_line(line)
            mote.set_pixel(line, led_index, 224, 64, 0, 1)
            mote.show()
            pixels.append([line, led_index, 224, 64, 0, 1])
            time.sleep(0.015)
        print(pixels)
        mote.clear()
        draw(pixels)
        pixels.clear()


x = 0
y = 1
r = 2
g = 3
b = 4
brightness = 5


def draw(pixels):
    for v in range(10, 1, -1):
        for pixel in pixels:
            mote.set_pixel(pixel[x], pixel[y], 255, 255, 255, v / 10)
            mote.show()
        time.sleep(0.1)
        mote.clear()
        mote.show()
        time.sleep(0.01)
    for pixel in pixels:
        mote.set_pixel(pixel[x], pixel[y], pixel[r], pixel[g], pixel[b], pixel[brightness])
        mote.show()
    time.sleep(1)
    mote.clear()
    mote.show()


if __name__ == '__main__':
    for _ in range(0, 1000):
        orange_lighting()
        wait_time = random.randint(1, 120)/10
        print('please wait ' + str(wait_time) + ' seconds')
        time.sleep(wait_time)

