from zeroeighttrack import leaderboard_utils, leaderboard_file

results = leaderboard_file.load_leaderboard_from_file()


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
    leaderboard_file.save_leaderboard_to_file(results)
    return len(results)


def sort_leaderboard_by_time() -> list:
    return sorted(results, key=lambda index: index['time_in_ds'], reverse=False)


def get_top10() -> list:
    all_result = sort_leaderboard_by_time()
    return all_result[:10]


def size() -> int:
    return len(results)


if __name__ == '__main__':
    # add_result('26.55.4--9.4.2020--1')
    print(sort_leaderboard_by_time())


def remove_result_by_id(result_id: int):
    results.pop(result_id-1)
    save_results()


def get_position_for_id(result_id):
    top_leaderboard = sort_leaderboard_by_time()
    x = {}
    for rank in top_leaderboard:
        if rank['id'] == result_id:
            x = rank
            break
    return  top_leaderboard.index(x)+1