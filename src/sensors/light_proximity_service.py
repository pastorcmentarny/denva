try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559

    ltr559 = LTR559()
except ImportError:
    import ltr559


def get_illuminance():
    return ltr559.get_lux()


def get_proximity():
    return ltr559.get_proximity()
