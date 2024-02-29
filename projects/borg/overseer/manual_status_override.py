import json
import logging
import logging.config
import os
import sys
from pathlib import Path

logger = logging.getLogger('overseer_mode')


def setup_logging():
    path = r'd:\denva\src\configs\overseer_mode.json'
    if os.path.exists(path):
        with open(path, 'rt') as config_json_file:
            config = json.load(config_json_file)
        logging.config.dictConfig(config)
        logging.captureWarnings(True)
        logger.info(f'logs loaded from {path}')
    else:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)
        logger.warning(f'Using default logging due to problem with loading from log: {path}')


if __name__ == '__main__':
    setup_logging()
    status_filepath = Path(r"D:\overseer_mode.txt")
    with open(status_filepath, 'w') as status_file:
        if len(sys.argv) == 2:
            logger.info(f'Updating {sys.argv[0]} with {sys.argv[1]}')
            status_file.write(str(sys.argv[1]))
        else:
            logger.info(f'Setting back to auto mode')
            status_file.write("")
