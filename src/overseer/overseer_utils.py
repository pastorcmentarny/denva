def set_color_for(color_name: str):
    if color_name in colors:
        red, green, blue = colors.get(color_name)
        change_to(red, green, blue)
    else:
        logger.warning(f'I need supported color not {color_name}')
        return 'rubbish'


def change_to(red: int, green: int, blue: int, brightness=0.4):
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, red, green, blue, brightness)
    mote.show()