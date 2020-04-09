from eighttrack import leaderboard_utils, leaderboard_file

results = [
    {
        'date': '1.4',
        'time': '24.46.3',
        'time_in_ds': 14863,
        'lap': 1,
        'id': 3
    }, {
        'date': '1.4',
        'time': '21.38.8',
        'time_in_ds': 12988,
        'lap': 2,
        'id': 4
    }, {
        'date': '31.3',
        'time': '26.21.9',
        'time_in_ds': 15819,
        'lap': 1,
        'id': 2
    }, {
        'date': '30.3',
        'time': '30.53.1',
        'time_in_ds': 18531,
        'lap': 1,
        'id': 1
    }, {
        'date': '6.4',
        'time': '24.46.3',
        'time_in_ds': 14863,
        'lap': 1,
        'id': 5
    }, {
        'date': '7.4',
        'time': '25.21.9',
        'time_in_ds': 15219,
        'lap': 1,
        'id': 6
    }
]


def get_result_by_id(result_id: int) -> dict:
    for result in results:
        if result['id'] == result_id:
            return result
    return {}

def save_results():
    leaderboard_file.save_leaderboard_to_file(results)

def load_results() -> list:
    return results


def add_result(lap_result: str) -> int:
    result_as_dict = leaderboard_utils.convert_lap_result_request_to_dict(lap_result, len(results) + 1)
    results.append(result_as_dict)
    return len(results)


def sort_leaderboard_by_time() -> list:
    return sorted(results, key=lambda index: index['time_in_ds'], reverse=False)

def get_top10() -> list:
    all_result = sort_leaderboard_by_time()
    return all_result[:10]

if __name__ == '__main__':
    save_results()