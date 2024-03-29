import logging

from mote import Mote

import rain_effect, alert_effect, overseer_utils
import overseer_config, idle_effect, fire_effect, party_effect, lighting_effect, night_fire_storm_mode
import borg_effect

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
    idle_effect.turn_light_off(mote)


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
    idle_effect.turn_light_off(mote)


def party_random_color_mode():
    party_effect.random_color_mode(mote)


def orange_lighting():
    return lighting_effect.orange_lighting(mote)


def lunch_effect():
    fire_effect.show_on_display(mote)
