import logging
import time

logger = logging.getLogger('overseer')


def show_on_display(red: int, green: int, blue: int, mote):
    logger.info(f'Going into knight rider mode using [{red}-{green}-{blue}]')
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(5):
        for line_index in range(0, 16):
            mote.clear()
            for line_led in range(1, 5):
                mote.set_pixel(line_led, line_index, red, green, blue, 0.4)
                if line_index > 0:
                    mote.set_pixel(line_led, line_index - 1, red, green, blue, 0.3)
                if line_index > 1:
                    mote.set_pixel(line_led, line_index - 2, int(red / 2), int(green / 2), int(blue / 2), 0.25)
                if line_index > 2:
                    mote.set_pixel(line_led, line_index - 3, int(red / 2), int(green / 2), int(blue / 2), 0.2)
            mote.show()
            time.sleep(0.1)

        for line_index in range(15, -1, -1):
            mote.clear()
            for line_led in range(1, 5):
                mote.set_pixel(line_led, line_index, red, green, blue, 0.4)
                if line_index < 15:
                    mote.set_pixel(line_led, line_index + 1, red, green, blue, 0.3)
                if line_index < 14:
                    mote.set_pixel(line_led, line_index + 2, int(red / 2), int(green / 2), int(blue / 2), 0.25)
                if line_index < 13:
                    mote.set_pixel(line_led, line_index + 3, int(red / 2), int(green / 2), int(blue / 2), 0.2)
            mote.show()
            time.sleep(0.1)
