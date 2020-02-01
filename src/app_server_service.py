import datetime

import time

import www.celebrations as celebrations
import www.random_chinese_word as cn
import www.good_english_sentence as eng
import www.good_method_name as method
import www.random_irregular_verb as verb
import utils
import web_data


def get_last_updated_page() -> str:
    now = datetime.datetime.now()
    return "{}.{}'{} - {}:{}".format(now.day,now.month,now.year,now.hour,now.minute)


def get_gateway_data() -> dict:
    return {'chinese' : cn.get_random_chinese_word(),
            'english' : eng.get_random_english_sentence(),
            'verb' : verb.get_random_irregular_verb(),
            'method' : method.get_random_method_name(),
            'calendar' : celebrations.get_next_3_events(),
            'today' : get_last_updated_page(),
            'weather' : "Weather:Maximum daytime temperature: 7 degrees Celsius;Minimum nighttime temperature: 6 degrees Celsius.Overcast.Sunrise: 07:51; Sunset: 16:38.UV: Low;Pollution: Low;No pollen data.", # web_data.get_weather()
            }


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
