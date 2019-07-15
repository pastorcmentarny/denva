def uv_description(logging, uv_index):
    if uv_index == 0:
        return "NONE"
    elif uv_index < 3:
        return "LOW"
    elif 3 <= uv_index < 6:
        return "MEDIUM"
    elif 6 <= uv_index < 8:
        return "HIGH"
    elif 8 <= uv_index < 11:
        return "VERY HIGH"
    elif uv_index > 11:
        return "EXTREME"
    else:
        logging.warning('weird uv value: {}'.format(uv_index))
        return "UNKNOWN"


def get_brightness(logging, r, g, b) -> str:
    max_value = max(r, g, b)
    mid = (r + g + b) / 3
    result = (max_value + mid) / 2

    if result < 16:
        return 'pitch black'
    elif 32 <= result < 64:
        return 'very dark'
    elif 64 <= result < 96:
        return 'dark'
    elif 96 <= result < 128:
        return 'bit dark'
    elif 128 <= result < 160:
        return 'grey'
    elif 160 <= result < 192:
        return 'bit bright'
    elif 192 <= result < 224:
        return 'bright'
    elif 224 <= result < 240:
        return 'very bright'
    elif 240 <= result < 256:
        return 'white'
    else:
        logging.warning('weird brightness value: {} for {} {} {}'.format(result, r, g, b))
        return '?'