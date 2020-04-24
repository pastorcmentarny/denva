from common import dom_utils


def generate_highscore_as_text(results: list, left_width=25, right_width=6) -> list:
    lines = []
    title = 'Current Highscore Table {}'.format(dom_utils.get_timestamp_title(with_time=False))
    lines.append(title.center(left_width + right_width, "-"))
    for result in results:
        lines.append(get_result_for(result, left_width, right_width))
    lines.append('-' * 41)
    lines.append('Zeroeight Track Info: Length: 2.6km. Ascent: 55m')
    return lines


def get_result_for(result: dict, left_width: int, right_width: int) -> str:
    title = 'Id:{} @ {} [Lap:{}]'.format(result['id'], result['date'], result['lap'])
    value = ' {} ds.'.format(result['time'])
    return title.ljust(left_width, '.') + str(value).rjust(right_width, ' ')
