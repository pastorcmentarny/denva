import bs4
import json
import requests


def get_train() -> str:
    response = requests.get('https://www.nationalrail.co.uk/service_disruptions/indicator.aspx')
    train_status = ''
    try:
        response.raise_for_status()  # without try it will exit program
        html_manager = bs4.BeautifulSoup(response.text, "html.parser")

        response = html_manager.select('tr.accordian-header')
        x = response[2].find_all('td')
        train_status += x[0].text.replace(' Railways', '') + ': ' + x[1].text
    except Exception as whoops:
        print('Unable to get weather temperature due to : %s' % whoops)
    return train_status


def get_tube():
    response = requests.get('https://api.tfl.gov.uk/line/mode/tube/status')
    data = json.loads(response.text)
    tubes = []
    for i in data:
        if i['id'] == 'metropolitan' or i['id'] == 'jubilee' or i['id'] == 'victoria':
            text = i['id'].capitalize() + ': '
            for status in i['lineStatuses']:
                text += status['statusSeverityDescription']
            tubes.append(text)
    return tubes


def get_status() -> list:
    statuses = get_tube()
    statuses.append(get_train())
    return statuses


# run without app
def main():
    statuses_list = get_status()
    for item in statuses_list:
        print(item)


if __name__ == '__main__':
    main()
