import logging
import time

from overseer import overseer_config

logger = logging.getLogger('overseer')


def red_alert(mote):
    logger.info('Going into red alert')
    display_alert_for(mote, overseer_config.RED)


def yellow_alert(mote):
    logger.info('Going into yellow alert')
    display_alert_for(mote, overseer_config.YELLOW)


def display_alert_for(mote, color: str):
    selected_color = overseer_config.colors.get(color)

    mote.set_brightness(0)
    for led_index in range(0, 16):
        for line_led in range(1, 5):
            mote.set_pixel(line_led, led_index, selected_color[0], selected_color[1], selected_color[2])

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
