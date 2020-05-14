"""
[
{"hex":"471f6f", "squawk":"0000", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":4975,  "vert_rate":1920,"track":69, "validtrack":1,"speed":190, "messages":3, "seen":231},
{"hex":"3c65c8", "squawk":"2565", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":0,  "vert_rate":-576,"track":89, "validtrack":1,"speed":127, "messages":4, "seen":248}
]
"""
import json
import logging
import time

from common import dom_utils
from gateways import local_data_gateway

logger = logging.getLogger('app')


def digest():
    report_file_path = "D:\\denva\\data\\aircraft-test.txt"

    while True: # run every 5 seconds if the same as last one

        result = local_data_gateway.get_data_for("http://192.168.0.201:16601/data.json", 5)
        result += "\n"
        print(result)
        logger.info('Saving report to {}'.format(report_file_path))
        with open(report_file_path, 'a+', encoding='utf-8') as report_file:
            json.dump(result, report_file, ensure_ascii=False, indent=4)
        time.sleep(5)


if __name__ == '__main__':
    dom_utils.setup_test_logging()
    digest()
