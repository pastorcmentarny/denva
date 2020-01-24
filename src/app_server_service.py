import datetime

import time

import utils
import web_data


def get_fasting_warning() -> str:
    hour = datetime.datetime.now().hour
    if hour >= 19 or hour <= 11:
        return "NO FOOD (INTERMITTENT FASTING PERIOD)"
    elif hour == 10:
        return "NO FOOD (OPTIONAL)"
    return None


def get_all_warnings_page() -> list:
    start = time.time_ns()
    data = []

    tube = web_data.get_tube(False)
    if tube == ["Tube data N/A"]:
        data.append("Tube data N/A")
    elif tube != 'Good Service' or tube != 'Service Closed':
        data.append(tube)

    train = web_data.get_train()
    if train == 'Train data N/A':
        data.append('Train data N/A')
    elif train != "Good service":
        data.append(train)

    data.append(get_fasting_warning())

    data = utils.clean_list_from_nones(data)

    end = time.time_ns()
    print('Execution time: {} ns.'.format((end - start)))

    return data


#USED for test only
if __name__ == '__main__':
    print(get_all_warnings_page())
