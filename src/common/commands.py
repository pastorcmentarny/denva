#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging
import re
import subprocess
import platform

import psutil

import config
import dom_utils

logger = logging.getLogger('app')


def get_cpu_speed():
    try:
        return psutil.cpu_freq()[0] + 'Mhz'
    except Exception as exception:
        logger.warning(f'Unable to get CPU speed due to :{exception}', exc_info=True)
        return 'Unknown MHz'


def get_cpu_temp() -> str:
    cmd = 'vcgencmd measure_temp'
    try:
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as ps:
            output = ps.communicate()[0]
            ps.kill()
            return output.decode(config.ENCODING).strip().replace('temp=', config.EMPTY)
    except Exception as exception:
        logger.warning(f'Process for get_cpu_speed() have NOT being assassinated due to :{exception}',
                       exc_info=True)
        return '0'


def get_cpu_temp_as_number() -> float:
    return float(dom_utils.get_float_number_from_text(get_cpu_temp()))


def get_ip() -> str:
    cmd = """hostname -I | awk '{print $1}'"""
    try:
        result = subprocess.check_output(cmd, shell=True)
        return str(result.strip(), config.ENCODING)
    except Exception as get_ip_exception:
        logger.error(f'Unable to get IP (Network down?) due to {get_ip_exception}')
        return "ERROR"


def get_uptime() -> str:
    return str(subprocess.check_output(['uptime', '-p']), config.ENCODING) \
        .strip() \
        .replace('weeks', 'w').replace('week', 'w') \
        .replace('days', 'd').replace('day', 'd') \
        .replace('hours', 'h').replace('hour', 'h') \
        .replace('minutes', 'm').replace('minute', 'm')


def get_system_info() -> dict:
    return {
        'Node': platform.node(),
        'OS': platform.platform(),
        'Python': platform.python_version(),
        'Processor': platform.processor(),
        'CPU Speed': get_cpu_speed(),
        'CPU Temp': get_cpu_temp(),
        'IP': get_ip(),
        'Uptime': get_uptime(),
        "Memory Available": f'{dom_utils.convert_bytes_to_megabytes(psutil.virtual_memory().available)} MB',
        'Free Space': f'{get_space_available()} MB'
    }


def get_space_available() -> str:
    try:
        with subprocess.Popen("df / -m --output=avail", stdout=subprocess.PIPE, shell=True) as p:
            result, _ = p.communicate()
            p.kill()
            return re.sub('[^0-9.]', config.EMPTY, str(result).strip())
    except Exception as space_available_exception:
        logger.error(f'Unable to available space due to {space_available_exception}')
        return "0"


def get_ram_available():
    return psutil.virtual_memory().available / 1000000


def get_lines_from_path(path: str, lines: int) -> dict:
    text = str(subprocess.check_output(['tail', '-n', str(lines), path]).strip(), config.ENCODING).split('\n')
    return dom_utils.convert_list_to_dict(text)


def get_last_line_from_log(path: str) -> str:
    text = str(subprocess.check_output(['tail', '-n', "1", path]).strip(), config.ENCODING)
    return text


def is_internet_up(hostname: str) -> bool:
    try:
        text = str(subprocess.check_output(['hostname', '-I']).strip(), config.ENCODING)
    except Exception as e:
        logger.error(f'Unable to check is internet up due to: {e}')
        return False
    return text == hostname


def reboot(reason: str):
    logger.warning(f"Rebooting device due to: {reason}")
    subprocess.check_output(['sudo', 'reboot'])
    return "Rebooting.."


def get_system_logs(number: int) -> dict:
    return get_lines_from_path('/var/log/syslog', number)


def is_dump_active():
    try:
        cmd = f'ps -aux | grep "./dump1090 --net --net-http-port 16601 --metric --quiet" | grep -v grep'
        result = subprocess.check_output(cmd, shell=True)
        logger.debug(f'Dump1090 is UP. Result {result}')
        return "OK"
    except Exception as e:
        logger.error(f'Dump1090 is DOWN due to {e}')
        return "ERROR"


def is_dump_digest_active():
    try:
        cmd = f"ps -aux | grep app_dump_data_digest.py | grep -v grep"
        result = subprocess.check_output(cmd, shell=True)
        logger.info(f'Result {result}')
        return "OK"
    except Exception as e:
        logger.error(f'Data digest for Dump1090 is DOWN due to {e}')
        return "ERROR"


def get_ping_results() -> dict:
    pages = config.get_ping_pages().copy()
    ping_result = {}
    for page in pages:
        cmd = """ping -qc 1 """ + page + """ 2>&1 | awk -F'/' 'END{ print (/^rtt/? "PASS "$5" ms":"FAIL") }'"""
        try:
            result = subprocess.check_output(cmd, shell=True)
            logger.debug(f'Ping {result}')
            ping_result.update({page: result})
        except Exception as e:
            logger.error(f'Unable to run ping test', exc_info=True)
            ping_result.update({page: str(e)})
    return ping_result
