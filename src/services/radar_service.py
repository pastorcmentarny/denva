from gateways import local_data_gateway


def get_aircraft_detected_today_count():
    result = local_data_gateway.get_current_reading_for_aircraft()
    if 'error' in result:
        return 'Unknown'
    else:
        return result["detected"]
