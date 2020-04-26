import random


def get_state_colour(current_state):
    if current_state.get_status_as_light_colour() == 'RED':
        color_red = 255
        color_green = 0
        color_blue = 0
    elif current_state.get_status_as_light_colour() == 'ORANGE':
        color_red = 255
        color_green = 110
        color_blue = 0
    else:
        color_red = 0
        color_green = 255
        color_blue = 0
    return color_red, color_green, color_blue


def get_random_pixel_location_at_night(x: int):
    return x + random.randint(0, 2)
