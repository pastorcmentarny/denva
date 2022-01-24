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
from datetime import datetime

import psutil

import dom_utils

logger = logging.getLogger('app')

step = 0.1
photo_dir = ''


def mount_all_drives(device: str = 'denva'):
    logger.info('mounting external partition for pictures')

    try:
        if device == 'denva':
            logger.info('Mounting local data partition..')
            cmd = 'sudo mount -t auto -v /dev/mmcblk0p3 /mnt/data'
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            logger.info(str(ps.communicate()[0]))
        logger.info('Mounting network(LattePanda) data partition..')
        cmd = 'sudo mount -a'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info(str(ps.communicate()[0]))
    except Exception as exception:
        error_message = "Unable to mount drive due to {}".format(exception)        
        logger.warning(f'Something went badly wrong..{error_message}', exc_info=True)


# TODO remove it
def get_cpu_speed():
    cmd = "find /sys/devices/system/cpu/cpu[0-3]/cpufreq/scaling_cur_freq -type f | xargs cat | sort | uniq -c"
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as ps:
        output = ps.communicate()[0]
        output = str(output)
        output = output.strip()[4:len(output) - 3].strip()[2:]  # i am sorry ..

        try:
            ps.kill()
        except Exception as exception:
            logger.warning('Process for get_cpu_speed() have NOT being assassinated due to :{}'.format(exception),
                           exc_info=True)

    try:
        output = str(float(output) / 1000)
    except ValueError:
        logger.warning(output)
        return 'CPU: variable speed'

    return output + ' Mhz'


def get_cpu_temp() -> str:
    cmd = '/opt/vc/bin/vcgencmd measure_temp'
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as ps:
        output = ps.communicate()[0]
        try:
            ps.kill()
        except Exception as exception:
            logger.warning('Process for get_cpu_speed() have NOT being assassinated due to :{}'.format(exception),
                           exc_info=True)

        return str(output).strip().replace('temp=', '')


def get_cpu_temp_as_number() -> float:
    return float(dom_utils.get_float_number_from_text(get_cpu_temp()))


def get_ip() -> str:
    cmd = """hostname -I | awk '{print $1}'"""
    try:
        result = subprocess.check_output(cmd, shell=True)
        return str(result.strip(), "utf-8")
    except Exception as e:
        logger.error('Unable to get IP (Network down?) due to {}'.format(e))
        return "ERROR"


def get_uptime() -> str:
    return str(subprocess.check_output(['uptime', '-p']), "utf-8") \
        .strip() \
        .replace('weeks', 'w').replace('week', 'w') \
        .replace('days', 'd').replace('day', 'd') \
        .replace('hours', 'h').replace('hour', 'h') \
        .replace('minutes', 'm').replace('minute', 'm')


def get_system_info() -> dict:
    return {
        'CPU Speed': get_cpu_speed(),
        'CPU Temp': '{} °C'.format(get_cpu_temp_as_number()).encode('utf-8'),
        'IP': get_ip(),
        'Uptime': get_uptime(),
        "Memory Available": '{} MB'.format(dom_utils.convert_bytes_to_megabytes(psutil.virtual_memory().available)),
        'Free Space': '{} MB'.format(get_space_available()),
        'Data Free Space': '{} MB'.format(get_data_space_available())
    }


def get_space_available():
    with subprocess.Popen("df / -m --output=avail", stdout=subprocess.PIPE, shell=True) as p:
        result, _ = p.communicate()
        p.kill()
        return re.sub('[^0-9.]', '', str(result).strip())


def get_data_space_available():
    with subprocess.Popen("df /mnt/data -m --output=avail", stdout=subprocess.PIPE, shell=True) as p:
        result, _ = p.communicate()
        p.kill()
        return re.sub('[^0-9.]', '', str(result).strip())


def get_lines_from_path(path: str, lines: int) -> dict:
    text = str(subprocess.check_output(['tail', '-n', str(lines), path]).strip(), "utf-8").split('\n')
    return dom_utils.convert_list_to_dict(text)


def get_last_line_from_log(path: str) -> str:
    text = str(subprocess.check_output(['tail', '-n', "1", path]).strip(), "utf-8")
    return text


def get_last_photo_filename() -> str:
    current_time = datetime.now()
    cmd = f"ls /mnt/data/photos/{current_time.year}/{current_time.month:02d}/{current_time.day:02d}/ -rt | tail -1"
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as ps:
        result = ps.communicate()[0]
        ps.kill()
        return str(result, 'utf-8')


def reboot(reason: str):
    logger.warning("Rebooting device due to: {}".format(reason))
    subprocess.check_output(['sudo', 'reboot'])
    return "Rebooting.."


def halt(device: str):
    logger.warning("Halting {} device for safe shutdown".format(device))
    subprocess.check_output(['sudo', 'halt'])
    return "Preparing {} device for safe shutdown".format(device)


def get_system_logs(number: int) -> dict:
    return get_lines_from_path('/var/log/syslog', number)


def is_dump_active():
    try:
        cmd = f'ps -aux | grep "./dump1090 --net --net-http-port 16601 --metric --quiet" | grep -v grep'
        result = subprocess.check_output(cmd, shell=True)
        logger.debug('Dump1090 is UP. Result {}'.format(result))
        return "UP"
    except Exception as e:
        logger.error('Dump1090 is DOWN due to {}'.format(e))
        return "DOWN"


def is_dump_digest_active():
    try:
        cmd = f"ps -aux | grep app_dump_data_digest.py | grep -v grep"
        result = subprocess.check_output(cmd, shell=True)
        logger.info('Result {}'.format(result))
        return "UP"
    except Exception as e:
        logger.error('Data digest for Dump1090 is DOWN due to {}'.format(e))
        return "DOWN"


# TODO test 5 website and all Pi (and maybe laptops)
def get_ping_results() -> str:
    cmd = """ping -qc 1 google.com 2>&1 | awk -F'/' 'END{ print (/^rtt/? "PASS "$5" ms":"FAIL") }'"""
    try:
        result = subprocess.check_output(cmd, shell=True)
        logger.debug('Ping {}'.format(result))
        return str(result.strip(), "utf-8")
    except Exception as e:
        logger.error('Data digest for Dump1090 is DOWN due to {}'.format(e))
        return "ERROR"
