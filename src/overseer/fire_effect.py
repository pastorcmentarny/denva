import logging
import random

from overseer import lighting_effect, overseer_utils

logger = logging.getLogger('overseer')

def show_on_display(mote):
    for _ in range(1, 10):
        for _ in range(1, 3):
            overseer_utils.transform(mote)

        probability = random.randint(1, 100)
        if probability > 96:
            for _ in range(1, probability):
                lighting_effect.lighting(mote)
        elif probability > 88:
            lighting_effect.rainbow_lighting(mote)
        elif probability > 80:
            lighting_effect.lighting(mote)