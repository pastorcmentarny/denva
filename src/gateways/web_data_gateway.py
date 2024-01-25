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
import json
import logging
import bs4
import requests
from datetime import datetime
from gateways import local_data_gateway

logger = logging.getLogger('app')
ENCODING = 'utf-8'


def get_train() -> str:
    return "Disabled"
    logger.info('Getting Chiltern Railways data..')
    try:
        response = requests.get('https://www.nationalrail.co.uk/service_disruptions/indicator.aspx', timeout=5)
        log_response_result(response, 'trains')
        train_status = ''
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        response = html_manager.select('tr.accordian-header')
        train_tag = response[3].find_all('td')
        train_status += train_tag[0].text.replace(' Railways', '') + ': ' + train_tag[1].text
        if "Good service" not in train_status:
            local_data_gateway.add_entry_to_diary("Disruption on the Chiltern Railways. {}".format(train_tag[1].text))
    except Exception as whoops:
        logger.error('Unable to get train data due to : %s' % whoops)
        train_status = 'Train data N/A'
    return train_status


def get_timestamp_for_data_row(dt):
    return f"{dt.year}{dt.month:02d}{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}"


def get_tube_statuses_from_url():
    tubes = []
    try:
        response = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
        data = json.loads(response.text)
        for i in data:
            for status in i['lineStatuses']:
                text = f"{get_timestamp_for_data_row(datetime.now())} :: {i['id'].capitalize()}::{status['statusSeverityDescription']}"
                tubes.append(text)
    except Exception as whoops:
        print('Unable to get tube data due to : %s' % whoops)
        tubes = ['Tube data N/A']
    return tubes


def get_status() -> list:
    statuses = get_tube(True)
    statuses.append(get_train())
    return statuses


def get_tube(online: bool):
    logger.info('Getting tube data..')
    try:
        response = requests.get('https://api.tfl.gov.uk/line/mode/tube/status', timeout=4)
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
                            local_data_gateway.add_entry_to_diary(
                                "{} has {} due to {}".format(i['id'], status['statusSeverityDescription'],
                                                             status['reason']))
                tubes.append(text)
            else:
                for status in i['lineStatuses']:
                    if ('Good Service' not in status['statusSeverityDescription']) or (
                            'Service Closed' not in status['statusSeverityDescription']):
                        if 'reason' in status and online:
                            local_data_gateway.add_entry_to_diary(
                                f"{i['id']} has {status['statusSeverityDescription']} due to {status['reason']}")

    except Exception as whoops:
        logger.error('Unable to get tube data due to : %s' % whoops)
        tubes = ['Tube data N/A']
    return tubes


def get_crime() -> str:
    logger.info('Getting Crime data..')
    try:
        with requests.get('https://www.police.uk/hertfordshire/C02/crime/', timeout=5) as response:
            log_response_result(response, 'crime')
            html_manager = bs4.BeautifulSoup(response.text, "html.parser")

            crime_number = html_manager.select('p#no_location_crimes strong')[0].text
            crime_period = html_manager.select('#month > optgroup:nth-child(1) > option:nth-child(1)')[0].text
            crime_result = '{} crimes {}'.format(crime_number, crime_period)
            local_data_gateway.add_entry_to_diary(crime_result)
            return crime_result
    except Exception as whoops:
        logger.error('Unable to get crime data due to : %s' % whoops)
        return 'Crime data N/A'


def get_flood() -> str:
    logger.info('Getting Flood data..')
    try:
        with requests.get('https://flood-warning-information.service.gov.uk/warnings?location=Rickmansworth',
                          timeout=5) as response:
            log_response_result(response, 'flood')
            html_manager = bs4.BeautifulSoup(response.text, "html.parser")

            severe_flood_warnings = html_manager.select('#severe-flood-warnings')[0].text.replace(
                'Severe flood warnings',
                '').replace(
                'Severe flooding - danger to life', '').strip() + ' severe flooding warnings that are danger to life'
            flood_warnings = html_manager.select('#flood-warnings')[0].text.replace('Flood warnings', '').replace(
                'Flooding is expected - immediate action required',
                '').strip() + ' flooding warnings that require immediate action'
            flood_alerts = html_manager.select('#flood-alerts')[0].text.replace('Flood alerts', '').replace(
                'Flooding is possible - be prepared', '').strip() + ' flooding alerts that flooding is possible'
            flooding_result = "Flooding. {}, {}, {}.".format(severe_flood_warnings, flood_warnings, flood_alerts)
            local_data_gateway.add_entry_to_diary(flooding_result)
            return flooding_result
    except Exception as whoops:
        logger.error('Unable to get flood data due to : %s' % whoops)
        return 'Flood data N/A'


def get_weather() -> str:
    logger.info('Getting weather data..')
    try:
        with requests.get('https://www.metoffice.gov.uk/weather/forecast/gcptv0ryg', timeout=5) as response:
            response.encoding = ENCODING
            log_response_result(response, 'weather')

            html_manager = bs4.BeautifulSoup(response.text, "html.parser")

            weather = html_manager.select('#tabDay0')[0].find('div').text
            local_data_gateway.add_entry_to_diary(weather)
            return weather
    except Exception as whoops:
        logger.error('Unable to get weather data due to: {}'.format(whoops))
        return 'Weather data N/A'


def get_o2_status() -> str:
    logger.info(f'Getting o2 status')
    try:
        with requests.get(
                'https://status.o2.co.uk/api/care/2010-11-22/outages/near/radius/-1/lon/-0.5057294/lat/51.6367404/service/0/operator/0/ctype/10/address/wd38ql/customer/e1kGKHRsWmAycFN9JH4rdhsxE1gBXHlRdC0/auth/A5FDC03C:::620B3907?uuid=8d40762059154803b6dee4391394666c&browser_uuid=4a9f19cbf4fb488e8ba81e6994e89731&id=0b1b8c44-6800-9e4d-61a3-4935d46b5bc1',
                timeout=5) as response:
            html_manager = bs4.BeautifulSoup(response.text, "html.parser")

            log_response_result(response, "o2")
            o2_data = json.loads(str(html_manager))
            status = o2_data['outage_script_txt']
            local_data_gateway.add_entry_to_diary(status)
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


def _get_scale_result_from(city: str, index: int) -> str:
    if index > 300:
        level = 'Hazardous!'
        advice = 'Stay at home!'
    elif index > 150:
        level = 'Unhealthy'
        advice = 'Should stay at home.'
    elif index > 100:
        level = 'Moderate'
        advice = 'Limit prolong outdoor activity.'
    else:
        level = 'Good'
        advice = ""
    return 'At {}, pollution level is {} ({}).{}'.format(city.capitalize(), level, index, advice)


def get_pollution_for(city: str) -> str:
    logger.info(f'Getting pollution index for {city} ')
    try:
        with requests.get('https://aqicn.org/city/{}/'.format(city), timeout=5) as response:
            response.encoding = ENCODING
            log_response_result(response, 'weather')

            html_manager = bs4.BeautifulSoup(response.text, "html.parser")

            index = html_manager.select('.aqivalue')[0].text
            pollution_index = int(index)
            local_data_gateway.add_entry_to_diary(f"Polution index for {city} is {pollution_index}")
            return _get_scale_result_from(city, pollution_index)
    except Exception as whoops:
        logger.error('Unable to get pollution data due to: {}'.format(whoops))
        return 'Pollution data N/A'


def get_iss_location() -> dict:
    url = 'http://api.open-notify.org/iss-now.json'
    logger.info(f'Getting data about ISS location from {url}')
    try:
        with requests.get(url, timeout=5) as response:
            response.encoding = ENCODING
            log_response_result(response, 'ISS')
            print(json.loads(response.text))
            return json.loads(response.text)
    except Exception as whoops:
        logger.error('Unable to get ISS location data due to: {}'.format(whoops))
        return {'error': 'ISS location data N/A'}


def check_pages(headers, ok, pages, problems):
    for page in pages:
        logger.info('checking connection to :{}'.format(page))

        try:
            with requests.get(page, headers=headers, timeout=5) as response:
                if response.status_code == 200:
                    ok += 1
                else:
                    response.raise_for_status()

        except Exception as whoops:
            logger.warning('Response error: {}'.format(whoops))
            problems.append(whoops)

    return ok
