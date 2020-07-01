
def to_x(i: int) -> int:
    return 15 - i


def set_all_pixel_to(red: int, green: int, blue: int, display):
    for coordinate_x in range(0, 16):
        for coordinate_y in range(0, 16):
            display.set_pixel(coordinate_x, coordinate_y, red, green, blue)
