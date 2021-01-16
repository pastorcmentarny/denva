from datetime import datetime


def get_timer_for_fasting() -> int:
    if datetime.now().hour < 12:
        return 12 - 1 - datetime.now().hour
    else:
        time_left = 12 - 1 + (24 - datetime.now().hour)
        return 16 if time_left > 16 else time_left


def get_timer_for_eating() -> int:
    if is_default_fasting_time():
        return 0
    else:
        leds = 19 - 1 - datetime.now().hour
        leds *= 2
        if datetime.now().minute < 30:
            leds += 1
        return leds


def is_default_fasting_time() -> bool:
    return datetime.now().hour > 18 or datetime.now().hour <= 12


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def is_busy() -> bool:
    return True


if __name__ == '__main__':
    print(get_timer_for_eating())
