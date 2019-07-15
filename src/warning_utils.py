import re


def get_warnings(data) -> dict:
    warnings = {}
    data['temp'] = float(data['temp'])
    if data['temp'] < 16:
        warnings['temp'] = 'Temperature is too low. Current temperature is: ' + str(data['temp'])
    elif data['temp'] < 18:
        warnings['temp'] = 'Temperature is low. Current temperature is: ' + str(data['temp'])
    elif data['temp'] > 25:
        warnings['temp'] = 'Temperature is high. Current temperature is: ' + str(data['temp'])
    elif data['temp'] > 30:
        warnings['temp'] = 'Temperature is too high. Current temperature is: ' + str(data['temp'])

    data['humidity'] = float(data['humidity'])

    if data['humidity'] < 30:
        warnings['humidity'] = 'Humidity is too low. Current humidity is: ' + str(data['humidity'])
    elif data['humidity'] < 40:
        warnings['humidity'] = 'Humidity is low. Current humidity is: ' + str(data['humidity'])
    elif data['humidity'] > 60:
        warnings['humidity'] = 'Humidity is high. Current humidity is: ' + str(data['humidity'])
    elif data['humidity'] > 70:
        warnings['humidity'] = 'Humidity is too high. Current humidity is: ' + str(data['humidity'])

    data['uva_index'] = float(data['uva_index'])

    if data['uva_index'] > 6:
        warnings['uva_index'] = 'UV A is too high. Current UV A is: ' + str(data["uva_index"])

    data['uvb_index'] = float(data['uvb_index'])

    if data['uvb_index'] > 6:
        warnings['uvb_index'] = 'UV B is too high. Current UV B is: ' + str(data["uvb_index"])

    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > 75:
        warnings['cpu_temp'] = 'CPU temperature is too high. Current temperature is: ' + str(data['cpu_temp'])
    elif data['cpu_temp'] > 60:
        warnings['cpu_temp'] = 'CPU temperature is very high. Current temperature is: ' + str(data['cpu_temp'])
    elif data['cpu_temp'] > 50:
        warnings['cpu_temp'] = 'CPU temperature is high. Current temperature is: ' + str(data['cpu_temp'])

    if data['motion'] > 1000:
        warnings['motion'] = 'Dom is shaking his legs. Value: ' + str(data["motion"])

    return warnings
