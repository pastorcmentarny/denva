RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
PURPLE = [75, 0, 130]
WHITE = [255, 255, 255]
BLACK = [1, 1, 1]

colors = {
    'red': RED,
    'green': GREEN,
    'blue': BLUE,
    'purple': PURPLE,
    'white': WHITE,
    'black': BLACK
}


def get_color_for(color_name: str):
    if color_name in colors:
        r, g, b = colors.get(color_name)
        return f':{r}x{g}x{b}:'
    else:
        return 'rubbish'
