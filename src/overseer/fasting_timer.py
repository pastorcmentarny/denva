from datetime import datetime


def get_timer_for_fasting() -> int:
    return 0


def get_timer_for_eating () -> int:
    return 0


def is_default_fasting_time() -> bool:
    return datetime.now().hour > 18 or datetime.now().hour <= 12


def is_night_mode() -> bool:
    return datetime.now().hour >= 22 or datetime.now().hour < 6


def is_busy() -> bool:
    return True