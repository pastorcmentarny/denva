#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import subprocess
import time
import utils
logger = logging.getLogger('app')


def capture_picture() -> str:
    date = utils.get_timestamp_file()
    photo_path = "/home/pi/photos/{}.jpg".format(date)
    cmd = "fswebcam -r 1920x1080  --no-banner {}".format(photo_path)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(3) # improve it with check every 0.1 second
    return photo_path


def get_cpu_speed():
    cmd = "find /sys/devices/system/cpu/cpu[0-3]/cpufreq/scaling_cur_freq -type f | xargs cat | sort | uniq -c"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = str(output)
    output = output.strip()[4:len(output) - 3].strip()[2:]  # i am sorry ..
    try:
        output = str(float(output) / 1000)
    except ValueError:
        logger.warning(output)
        return 'CPU: variable speed'
    return output + ' Mhz'


def get_cpu_temp():
    return str(subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']), "utf-8") \
        .strip().replace('temp=', '')


def get_ip():
    text = str(subprocess.check_output(['ifconfig', 'wlan0']), "utf-8")
    start, end = text.find('inet'), text.find('netmask')
    result = text[start + 4: end]
    return 'IP:' + result.strip()


def get_uptime():
    return str(subprocess.check_output(['uptime', '-p']), "utf-8") \
        .strip() \
        .replace('weeks', 'w').replace('week', 'w') \
        .replace('days', 'd').replace('day', 'd') \
        .replace('hours', 'h').replace('hour', 'h') \
        .replace('minutes', 'm').replace('minute', 'm')


def get_system_info() -> dict:
    return {
        'CPU Speed': get_cpu_speed(),
        'CPU Temp': get_cpu_temp(),
        'IP': get_ip(),
        'Uptime': get_uptime(),
        'Free Space:': get_space_available() + 'MB'
    }


def get_space_available():
    p = subprocess.Popen("df / -m --output=avail", stdout=subprocess.PIPE, shell=True)
    result, _ = p.communicate()
    return re.sub('[^0-9.]', '', str(result).strip())


def get_last_ten_line_from_path(path: str) -> str:
    text = str(subprocess.check_output(['tail', '-n', "10", path]).strip(), "utf-8")
    return text


def get_last_line_from_log(path: str) -> str:
    text = str(subprocess.check_output(['tail', '-n', "1", path]).strip(), "utf-8")
    return text
