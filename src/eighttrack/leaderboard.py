results = [
    {
        'date': '1.4',
        'time': '24.46.3',
        'lap': 1,
        'id': 3
    }, {
        'date': '1.4',
        'time': '21.38.8',
        'lap': 2,
        'id': 4
    }, {
        'date': '31.3',
        'time': '26.21.9',
        'lap': 1,
        'id': 2
    }, {
        'date': '30.3',
        'time': '30.53.1',
        'lap': 1,
        'id': 1
    }, {
        'date': '6.4',
        'time': '24.46.3',
        'lap': 1,
        'id': 5
    }, {
        'date': '7.4',
        'time': '25.21.9',
        'lap': 1,
        'id': 6
    }
]

def get_result_by_id(result_id:int) -> dict:
    for result in results:
        if result['id'] == result_id:
            return result
    return {}


def load_results() -> list:
    return results
