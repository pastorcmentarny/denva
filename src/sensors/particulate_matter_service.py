import logging
import time

from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError

logger = logging.getLogger('app')

pms5003 = PMS5003()


def get_measurement():
    global pms5003
    p_1 = 0
    p_2 = 0
    p_10 = 0

    try:
        pms_data = pms5003.read()
    except pmsReadTimeoutError as exception:
        logger.warning("Failed to read PMS5003 due to: {}".format(exception), exc_info=True)
        logger.info('Restarting sensor.. (it will takes ... 5 seconds')
        pms5003 = PMS5003()
        time.sleep(5)
    else:
        p_1 = float(pms_data.pm_ug_per_m3(1.0))
        p_2 = float(pms_data.pm_ug_per_m3(2.5))
        p_10 = float(pms_data.pm_ug_per_m3(10))
    return p_1, p_2, p_10
