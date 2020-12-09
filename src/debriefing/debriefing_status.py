import random
import time

from mote import Mote

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()
mote.set_brightness(0.4)


def change_to(red: int, green: int, blue: int):
    for i in range(0, 16):
        for c in range(1, 5):
            mote.set_pixel(c, i, red, green, blue)
        time.sleep(0.05)
        mote.show()
    for i in range(0, 10):
        brightness = i / 10
        mote.set_brightness(brightness)
        time.sleep(0.02)
        mote.show()
    for i in range(9, 2, -1):
        brightness = i / 10
        mote.set_brightness(brightness)
        time.sleep(0.04)
        mote.show()
    time.sleep(0.5)


def red_alert():
    mote.set_brightness(0)
    for i in range(0, 16):
        for c in range(1, 5):
            mote.set_pixel(c, i, 255, 0, 0)

    for counter in range(0, 5):
        for b in range(0, 100):
            brightness = b / 100
            mote.set_brightness(brightness)
            time.sleep(0.02)
            mote.show()
        for d in range(99, -1, -1):
            brightness = d / 100
            mote.set_brightness(brightness)
            time.sleep(0.02)
            mote.show()


def yellow_alert():
    mote.set_brightness(0)
    for i in range(0, 16):
        for c in range(1, 5):
            mote.set_pixel(c, i, 144, 77, 0)

    for counter in range(0, 5):
        for b in range(0, 100):
            brightness = b / 100
            mote.set_brightness(brightness)
            time.sleep(0.03)
            mote.show()
        for d in range(99, -1, -1):
            brightness = d / 100
            mote.set_brightness(brightness)
            time.sleep(0.03)
            mote.show()


def purple_alert():
    mote.set_brightness(0)
    for i in range(0, 16):
        for c in range(1, 5):
            mote.set_pixel(c, i, 75, 0, 130)

    for counter in range(0, 10):
        for b in range(20, 45):
            brightness = b / 100
            mote.set_brightness(brightness)
            time.sleep(0.04)
            mote.show()
        for d in range(45, 24, -1):
            brightness = d / 100
            mote.set_brightness(brightness)
            time.sleep(0.03)
            mote.show()


def knight_rider(red: int, green: int, blue: int):
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(10):
        for i in range(0, 16):
            mote.clear()
            for c in range(1, 5):
                mote.set_pixel(c, i, red, green, blue, 0.4)
                if i > 0:
                    mote.set_pixel(c, i - 1, red, green, blue, 0.3)
                if i > 1:
                    mote.set_pixel(c, i - 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
                if i > 2:
                    mote.set_pixel(c, i - 3, int(red / 2), int(green / 2), int(blue / 2), 0.1)
            mote.show()
            time.sleep(0.1)

        for i in range(15, -1, -1):
            mote.clear()
            for c in range(1, 5):
                mote.set_pixel(c, i, red, green, blue, 0.4)
                if i < 15:
                    mote.set_pixel(c, i + 1, red, green, blue, 0.3)
                if i < 14:
                    mote.set_pixel(c, i + 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
                if i < 13:
                    mote.set_pixel(c, i + 3, int(red / 2), int(green / 2), int(blue / 2), 0.1)
            mote.show()
            time.sleep(0.1)


def christmas_mode():
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(100):
        speed = (random.randint(0, 20) / 100) + 0.01
        xmas_snow_colors = [[255, 0, 0], [0, 255, 0], [255, 255, 255]]
        red, green, blue = xmas_snow_colors[random.randint(0, len(xmas_snow_colors) - 1)]
        line = random.randint(1, 4)
        for i in range(0, 16):
            mote.clear()
            mote.set_pixel(line, i, red, green, blue, 0.4)
            if i > 0:
                mote.set_pixel(line, i - 1, red, green, blue, 0.3)
            if i > 1:
                mote.set_pixel(line, i - 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
            if i > 2:
                mote.set_pixel(line, i - 3, int(red / 4), int(green / 4), int(blue / 4), 0.1)
            mote.show()
            time.sleep(speed)


def run():
    xmas_counter = 1
    anti_xmas_counter = 1
    christmas_mode()
    while True:
        knight_rider(255, 0, 0)
        knight_rider(0, 255, 0)
        knight_rider(144, 70, 0)
        knight_rider(75, 0, 130)
        red_alert()
        yellow_alert()
        purple_alert()
        change_to(255, 0, 0)
        change_to(0, 255, 0)
        change_to(144, 70, 0)
        change_to(75, 0, 130)
        if bool(random.getrandbits(1)):
            print(f'Xmas l i g h t time ... Xmas :{xmas_counter} vs Anti: {anti_xmas_counter}')
            xmas_counter = xmas_counter + 1
            christmas_mode()
        else:
            print(f'No luck with xmas light this time :( ... Xmas :{xmas_counter} vs Anti: {anti_xmas_counter}')
            anti_xmas_counter = anti_xmas_counter + 1


if __name__ == '__main__':
    run()
