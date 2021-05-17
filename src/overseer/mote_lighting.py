import logging
import random
import time

from mote import Mote

from overseer import borg_effect, rain_effect, alert_effect, overseer_utils, \
    overseer_config, idle_effect, fire_effect

logger = logging.getLogger('overseer')

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()


def set_busy_mode():
    overseer_utils.set_color_for(mote, overseer_config.RED)


def party_mode():
    logger.info('Party time!')
    blink_speed = 0.02
    mote.set_brightness(0.4)
    for times in range(1000):
        for led_index in range(0, 16):
            for led_line in range(1, 5):
                mote.set_pixel(led_line, led_index, random.randint(0, 256), random.randint(0, 256),
                               random.randint(0, 256))
        mote.show()
        time.sleep(blink_speed)
        overseer_utils.set_color_for(mote, overseer_config.BLACK)
        mote.show()
        time.sleep(blink_speed)
    logger.info('Party is over.')


def turn_light_off():
    logger.info('Switching off light')
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, 0, 0, 0, 0)
    mote.clear()
    mote.set_brightness(0.1)


def borg():
    borg_effect.show_on_display(mote)


def red_alert():
    alert_effect.red_alert(mote)


def yellow_alert():
    alert_effect.yellow_alert(mote)


def rain():
    rain_effect.random_rain(mote)


def daydream():
    idle_effect.daydream(mote)


def fire_effect_with_lighting():
    fire_effect.show_on_display(mote)


def night_mode():
    idle_effect.night_mode(mote)
