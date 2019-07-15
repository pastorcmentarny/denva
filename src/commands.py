import subprocess


def get_cpu_temp():
    return str(subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']), "utf-8") \
        .replace('temp=', 'CPU:')


def get_cpu_speed():
    cmd = "find /sys/devices/system/cpu/cpu[0-3]/cpufreq/scaling_cur_freq -type f | xargs cat | sort | uniq -c"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = str(output)
    output = output.strip()[4:len(output) - 3].strip()[2:]  # i am sorry ..
    output = str(float(output) / 1000)
    return 'Cpu: ' + output + ' Mhz'

def get_ip():
    text = str(subprocess.check_output(['ifconfig', 'wlan0']), "utf-8")
    start, end = text.find('inet'), text.find('netmask')
    result = text[start+4: end]
    return 'IP:' + result.strip()