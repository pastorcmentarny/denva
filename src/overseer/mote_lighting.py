import logging

from mote import Mote

from overseer import borg_effect, rain_effect, alert_effect, overseer_utils, \
    overseer_config, idle_effect, fire_effect, party_effect

logger = logging.getLogger('overseer')

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()


def set_busy_mode():
    overseer_utils.set_color_for(mote, overseer_config.RED)


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


def party_random_color_mode():
    party_effect.random_color_mode(mote)
