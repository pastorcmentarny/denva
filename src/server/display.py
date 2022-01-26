import unicornhathd

unicornhathd.brightness(0.2)
unicornhathd.clear()


def reset_screen():
    for x in range(0, 16):
        for y in range(0, 16):
            unicornhathd.set_pixel(x, y, 0, 0, 0)
    unicornhathd.show()
