import logging
import random
from datetime import datetime

from overseer import lighting_effect, overseer_utils

logger = logging.getLogger('overseer')


def show_on_display(mote):
    for _ in range(1, 3):
        overseer_utils.transform(mote)

    if 0 <= datetime.now().hour < 6:
        probability = random.randint(1, 100)
        if probability > 96:
            for _ in range(1, probability):
                lighting_effect.lighting(mote)
        elif probability > 88:
            lighting_effect.rainbow_lighting(mote)
        elif probability > 80:
            lighting_effect.lighting(mote)
