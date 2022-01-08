import time

import config_service


def to_x(i: int) -> int:
    return 15 - i


def set_all_pixel_to(red: int, green: int, blue: int, display):
    for coordinate_x in range(0, 16):
        for coordinate_y in range(0, 16):
            display.set_pixel(coordinate_x, coordinate_y, red, green, blue)


def perform_blink_animation(unicornhathd):
    b1 = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19]
    b2 = [0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29]
    b3 = [0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39]
    b4 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49]
    b5 = [0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59]
    b6 = [0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69]
    brightnesses = [config_service.get_default_brightness_for_delight_display()]
    merge_brightnesses(brightnesses, [b3, b4, b5, b6])
    reverse_b1_to_b6(b1, b2, b3, b4, b5, b6)
    merge_brightnesses(brightnesses, [b6, b5, b4, b3, b2, b1])
    reverse_b1_to_b6(b1, b2, b3, b4, b5, b6)
    merge_brightnesses(brightnesses, [b1, b2])

    for x in range(0, 15):
        for b in brightnesses:
            unicornhathd.brightness(b)
            unicornhathd.show()
            time.sleep(0.025)


def merge_brightnesses(brightnesses, brightness_list):
    for brightness in brightness_list:
        brightnesses.extend(brightness)


def reverse_b1_to_b6(b1, b2, b3, b4, b5, b6):
    b1.reverse()
    b2.reverse()
    b3.reverse()
    b4.reverse()
    b5.reverse()
    b6.reverse()
