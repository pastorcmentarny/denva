#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import json
import logging

import bs4
import requests

stats_log = logging.getLogger('stats')
logger = logging.getLogger('app')


def get_train() -> str:
    logger.info('Getting Chiltern Railways data..')
    try:
        response = requests.get('https://www.nationalrail.co.uk/service_disruptions/indicator.aspx')
        log_response_result(response, 'trains')
        train_status = ''
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        response = html_manager.select('tr.accordian-header')
        train_tag = response[3].find_all('td')
        train_status += train_tag[0].text.replace(' Railways', '') + ': ' + train_tag[1].text
        if "Good service" not in train_status:
            stats_log.warning("Disruption on the Chiltern Railways. {}".format(train_tag[1].text))
    except Exception as whoops:
        logger.error('Unable to get train data due to : %s' % whoops)
        train_status = 'Train data N/A'
    return train_status


def get_tube(online: bool):
    logger.info('Getting tube data..')
    try:
        response = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
        log_response_result(response, 'tube')

        data = json.loads(response.text)
        tubes = []
        for i in data:
            if i['id'] == 'metropolitan' or i['id'] == 'jubilee' or i['id'] == 'victoria':
                text = i['id'].capitalize() + ': '
                for status in i['lineStatuses']:
                    text += status['statusSeverityDescription']
                    if 'reason' in status and online:
                        text += 'reason :' + status['reason']
                        if ('Good Service' not in status['statusSeverityDescription']) or (
                                'Service Closed' not in status['statusSeverityDescription']):
                            stats_log.warning("{} has {} due to {}".format(i['id'], status['statusSeverityDescription'],
                                                                           status['reason']))
                tubes.append(text)
            else:
                for status in i['lineStatuses']:
                    if ('Good Service' not in status['statusSeverityDescription']) or (
                            'Service Closed' not in status['statusSeverityDescription']):
                        if 'reason' in status and online:
                            stats_log.warning("{} has {} due to {}".format(i['id'], status['statusSeverityDescription'],
                                                                           status['reason']))

    except Exception as whoops:
        logger.error('Unable to get tube data due to : %s' % whoops)
        tubes = ['Tube data N/A']
    return tubes


def get_status() -> list:
    statuses = get_tube(True)
    statuses.append(get_train())
    return statuses


def get_crime() -> str:
    logger.info('Getting Crime data..')
    try:
        response = requests.get('https://www.police.uk/hertfordshire/C02/crime/')
        log_response_result(response, 'crime')
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        crime_number = html_manager.select('p#no_location_crimes strong')[0].text
        crime_period = html_manager.select('#month > optgroup:nth-child(1) > option:nth-child(1)')[0].text
        crime_result = '{} crimes {}'.format(crime_number, crime_period)
        stats_log.info(crime_result)
        return crime_result
    except Exception as whoops:
        logger.error('Unable to get crime data due to : %s' % whoops)
        return 'Crime data N/A'


def get_flood() -> str:
    logger.info('Getting Flood data..')
    try:
        response = requests.get('https://flood-warning-information.service.gov.uk/warnings?location=Rickmansworth')
        log_response_result(response, 'flood')
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        severe_flood_warnings = html_manager.select('#severe-flood-warnings')[0].text.replace('Severe flood warnings',
                                                                                              '').replace(
            'Severe flooding - danger to life', '').strip() + ' severe flooding warnings that are danger to life'
        flood_warnings = html_manager.select('#flood-warnings')[0].text.replace('Flood warnings', '').replace(
            'Flooding is expected - immediate action required',
            '').strip() + ' flooding warnings that require immediate action'
        flood_alerts = html_manager.select('#flood-alerts')[0].text.replace('Flood alerts', '').replace(
            'Flooding is possible - be prepared', '').strip() + ' flooding alerts that flooding is possible'
        flooding_result = "Flooding. {}, {}, {}.".format(severe_flood_warnings, flood_warnings, flood_alerts)
        stats_log.info(flooding_result)
        return flooding_result
    except Exception as whoops:
        logger.error('Unable to get flood data due to : %s' % whoops)
        return 'Flood data N/A'


def cleanup_weather_data(weather: str) -> list:
    weather = weather.splitlines()[1:]
    weather_result = 'Weather:'
    for sentence in weather:
        weather_result += sentence
    return weather_result


def clean_temp(temp: str) -> str:
    return temp.replace('\xa0', '').replace('\xc2', '').replace('\xb0', '')[0:(len(temp) - 4)] + '°C'


# prototype for cleanup data coming from weather website
def __get_mocked_weather():
    result = "Weather:Maximum daytime temperature: 7 degrees Celsius;Minimum nighttime temperature: 6 degrees Celsius.Overcast.Sunrise: 07:51; Sunset: 16:38.UV: Low;Pollution: Low;No pollen data."
    result = result.split(';')
    result_list = []
    for x in result:
        y = x.split('.')
        for z in y:
            result_list.append(z)
    print(result_list[0])
    result_list[0] = result_list[0].replace('Weather:', '')
    result_list.remove('')
    result_list.remove('Overcast')
    print(result_list)
    return result_list


def get_weather() -> list:
    if True:
        return __get_mocked_weather()

    logger.info('weather')
    try:
        response = requests.get('https://www.metoffice.gov.uk/weather/forecast/gcptv0ryg')
        response.encoding = "utf-8"
        log_response_result(response, 'weather')

        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        weather = html_manager.select('#tabDay0')[0].find('div').text
        stats_log.info(weather)
        return cleanup_weather_data(weather)
    except Exception as whoops:
        logger.error('Unable to get weather data due to: {}'.format(whoops))
        return ['Weather data N/A']


def get_o2_status() -> str:
    try:
        response = requests.get(
            'https://status.o2.co.uk/api/care/2010-11-22/outages/near/radius/-1/lon/-0.5057294/lat/51.6367404/service/0/operator/0/ctype/10/address/wd38ql/customer/e1kGKHRsWmAycFN9JH4rdhsxE1gBXHlRdC0/auth/A5FDC03C:::620B3907?uuid=8d40762059154803b6dee4391394666c&browser_uuid=4a9f19cbf4fb488e8ba81e6994e89731&id=0b1b8c44-6800-9e4d-61a3-4935d46b5bc1')
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")
        log_response_result(response)
        o2_data = json.loads(str(html_manager))
        status = o2_data['outage_script_txt']
        stats_log.info(status)
        return status
    except Exception as whoops:
        logger.error('Unable to get o2 data due to: {}'.format(whoops))
        return 'o2 data N/A'


def log_response_result(response, what: str):
    try:
        if response.status_code == 200:
            logger.debug('Received data from {}'.format(what))
        else:
            logger.warning(
                'There was a problem during receive data from {}. Return Code:{}'.format(what, response.status_code))
            response.raise_for_status()
    except Exception as whoops:
        logger.warning('Response error: {}'.format(whoops))


def main():
    print(get_weather())
    statuses_list = get_status()
    for item in statuses_list:
        print(item)


if __name__ == '__main__':
    get_weather()
