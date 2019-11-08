# -*- coding: utf-8 -*-
import bs4
import json
import logging
import requests

stats_log = logging.getLogger('stats')
logger = logging.getLogger('app')


def get_train() -> str:
    try:
        response = requests.get('https://www.nationalrail.co.uk/service_disruptions/indicator.aspx')
        train_status = ''
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        response = html_manager.select('tr.accordian-header')
        train_tag = response[2].find_all('td')
        train_status += train_tag[0].text.replace(' Railways', '') + ': ' + train_tag[1].text
        if "Good service" not in train_status:
            stats_log.warning("Disruption on the Chiltern Railways. {}".format(train_tag[1].text))
    except Exception as whoops:
        logger.error('Unable to get train data due to : %s' % whoops)
        train_status = 'Train data N/A'
    return train_status


def get_tube(online: bool):
    try:
        response = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
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
    try:
        response = requests.get('https://www.police.uk/hertfordshire/C02/crime/')
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        crime_number = html_manager.select('p#no_location_crimes strong')[0].text
        crime_period = html_manager.select('#month > optgroup:nth-child(1) > option:nth-child(1)')[0].text
        return crime_number + ' crimes ' + crime_period
    except Exception as whoops:
        logger.error('Unable to get crime data due to : %s' % whoops)
        train_status = 'Crime data N/A'
    return train_status


def get_flood() -> str:
    try:
        response = requests.get('https://flood-warning-information.service.gov.uk/warnings?location=Rickmansworth')
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        severe_flood_warnings = html_manager.select('#severe-flood-warnings')[0].text.replace('Severe flood warnings','').replace('Severe flooding - danger to life','').strip() + ' severe flooding warnings that are danger to life'
        flood_warnings = html_manager.select('#flood-warnings')[0].text.replace('Flood warnings','').replace('Flooding is expected - immediate action required','').strip() + ' flooding warnings that require immediate action'
        flood_alerts = html_manager.select('#flood-alerts')[0].text.replace('Flood alerts','').replace('Flooding is possible - be prepared','').strip() + ' flooding alerts that flooding is possible'
        return severe_flood_warnings + ", " + flood_warnings + ", " + flood_alerts
    except Exception as whoops:
        logger.error('Unable to get flood data due to : %s' % whoops)
        train_status = 'Flood data N/A'
    return train_status


def main():
    statuses_list = get_status()
    for item in statuses_list:
        print(item)


if __name__ == '__main__':
    main()
