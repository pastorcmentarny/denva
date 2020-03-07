import logging
from timeit import default_timer as timer

import requests

import data_files

PERFECT = 'Perfect'
GOOD = 'Good'
POOR = 'POOR'
DOWN = 'DOWN!'

logger = logging.getLogger('hc')


def network_check(in_china: bool = False) -> dict:
    logger.debug('Checking network...')
    ok = 0
    problems = []

    if in_china:
        problems.append("In China mode: {}".format(in_china))
        pages = [
            "https://dominiksymonowicz.com",
            'https://cn.bing.com/',
            'https://baidu.com',
            'https://amazon.cn',
            'https://www.cloudflare.com/zh-cn/',
            'https://www.sina.com.cn.'
        ]
    else:
        pages = [
            "https://dominiksymonowicz.com",
            'https://bing.com/',
            'https://baidu.com',
            'https://amazon.com',
            'https://wikipedia.org',
            'https://google.com/',
        ]
    headers = requests.utils.default_headers()
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    start_time = timer()

    for page in pages:

        print('checking connection to :{}'.format(page))

        try:
            response = requests.get(page, headers=headers)

            if response.status_code == 200:
                ok += 1
            else:
                response.raise_for_status()
        except Exception as whoops:
            logger.warning('Response error: {}'.format(whoops))
            problems.append(whoops)
    status = get_network_status(ok)

    end_time = timer()
    total_time = int(end_time - start_time) * 1000
    print("it took {} ms to check.".format(total_time))  # in ms
    log_result(problems, status, total_time)
    result = "{} of {} pages were loaded".format(ok, len(pages))

    logger.info(status)
    logger.info(result)
    if len(problems) > 0:
        logger.warning(problems)

    return {
        'status': status,
        'result': result,
        'problems': problems
    }


def log_result(problems, status, total_time):
    if status == POOR:
        logger.warning(
            'It looks like there is some problem with network as some pages failed to load due to: {}'.format(problems))
    if status == DOWN:
        logger.error('Network is DOWN! All services failed due to: {}'.format(problems))
    if status == PERFECT or status == GOOD:
        logger.debug('Network seems to be fine. I took {} ms to check.'.format(total_time))


def get_network_status(ok: int) -> str:
    if ok == 6:
        return PERFECT
    elif ok >= 4:
        return GOOD
    elif ok >= 2:
        return POOR
    else:
        return DOWN


if __name__ == '__main__':
    data_files.setup_logging()
    network_check()
