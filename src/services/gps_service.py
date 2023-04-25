import config


def check_warning(measurement: dict) -> list:
    warnings = []
    if float(measurement[config.FIELD_GPS_NUM_SATS]) < 1:
        warnings.append(f"GPS not detecting any satellites.")

    return warnings