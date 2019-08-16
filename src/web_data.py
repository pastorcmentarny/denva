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
        print('Unable to get train data due to : %s' % whoops)
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
        logger.warning('Unable to get tube data due to : %s' % whoops)
        tubes = ['Tube data N/A']
    return tubes


def get_status() -> list:
    statuses = get_tube(True)
    statuses.append(get_train())
    return statuses


# run without app
def main():
    statuses_list = get_status()
    for item in statuses_list:
        print(item)


if __name__ == '__main__':
    main()
