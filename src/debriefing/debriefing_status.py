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


def knight_rider():
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(10):
        for i in range(0, 16):
            mote.clear()
            for c in range(1, 5):
                mote.set_pixel(c, i, 75, 0, 130, 0.4)
                if i > 0:
                    mote.set_pixel(c, i-1, 75, 0, 130, 0.3)
                if i > 1:
                    mote.set_pixel(c, i-2, 50, 0, 85, 0.2)
                if i > 2:
                    mote.set_pixel(c, i-3, 50, 0, 85, 0.1)
            mote.show()
            time.sleep(0.1)

        for i in range(15, -1, -1):
            mote.clear()
            for c in range(1, 5):
                mote.set_pixel(c, i, 75, 0, 130, 0.4)
                if i < 15:
                    mote.set_pixel(c, i+1, 75, 0, 130, 0.3)
                if i < 14:
                    mote.set_pixel(c, i+2, 50, 0, 85, 0.2)
                if i < 13:
                    mote.set_pixel(c, i+3, 50, 0, 85, 0.1)
            mote.show()
            time.sleep(0.1)


def run():
    while True:
        knight_rider()
        red_alert()
        yellow_alert()
        purple_alert()
        change_to(255, 0, 0)
        change_to(0, 255, 0)
        change_to(144, 70, 0)
        change_to(75, 0, 130)


if __name__ == '__main__':
    run()
