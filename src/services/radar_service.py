from gateways import local_data_gateway


def get_aircraft_detected_today_count():
    result = local_data_gateway.get_current_reading_for_aircraft()
    if 'error' in result:
        return 'Unknown'
    else:
        return get_count_difference_to_yesterday(int(result["detected"]))


def get_count_difference_to_yesterday(count: int) -> str:
    result = local_data_gateway.get_yesterday_report_for_aircraft()
    if 'error' in result:
        return ''
    else:
        diff = count - int(result["detected"])
        if diff > 0:
            return ' {}(+{}↑)'.format(count, diff)
        elif diff == 0:
            return ''
        else:
            return ' {}({}↓)'.format(count, diff)
