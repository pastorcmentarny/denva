import random
import time
from datetime import datetime
from random import randint

from server import display

stars = []
stars_count = randint(1, 16)
for _ in range(stars_count):
    stars.append([randint(0, 10), randint(0, 15)])

grass_colour = randint(16, 112)

train_color = [75, 0, 130]
window_color = [224, 64, 0]
wheel_color = [64, 46, 64]
door_colour = [144, 222, 227]


def draw_star(star):
    if bool(random.getrandbits(1)):
        if bool(random.getrandbits(1)):
            grey = randint(0, 64)
            display.unicornhathd.set_pixel(star[0], star[1], grey, grey, grey)
        else:
            if bool(random.getrandbits(1)):
                if bool(random.getrandbits(1)):
                    display.unicornhathd.set_pixel(star[0], star[1], 96, 96, 96)
                else:
                    display.unicornhathd.set_pixel(star[0], star[1], 32, 32, 32)
            else:
                display.unicornhathd.set_pixel(star[0], star[1], 112, 112, 112)
    else:
        display.unicornhathd.set_pixel(star[0], star[1], 0, 0, 0)


def draw_stars():
    for star in stars:
        draw_star(star)


def draw_grass():
    for y in range(0, 16):
        display.unicornhathd.set_pixel(15, y, 0, grass_colour, 0)


moon_cycle = [[10, 2], [9, 2], [8, 2], [7, 2], [7, 3],
              [7, 4], [6, 4], [5, 5], [4, 6], [4, 7],
              [3, 8], [3, 9], [4, 9], [4, 10], [5, 10],
              [5, 11], [6, 11], [7, 11], [8, 11], [9, 11]]


def draw_moon():
    now = int(datetime.now().minute / 4)
    x, y = moon_cycle[now]
    display.unicornhathd.set_pixel(x, y, 112, 32, 0)
    display.unicornhathd.set_pixel(x, y + 1, 112, 32, 0)
    display.unicornhathd.set_pixel(x, y + 2, 32, 8, 0)
    display.unicornhathd.set_pixel(x + 1, y + 1, 32, 8, 0)
    for b in range(x + 1, x + 4):
        display.unicornhathd.set_pixel(b, y - 1, 112, 32, 0)
        for a in range(y, y + 4):
            display.unicornhathd.set_pixel(b, a, 0, 0, 0)
    if 15 >= x + 4 >= 0 and 15 >= y >= 0:
        display.unicornhathd.set_pixel(x + 4, y, 112, 32, 0)
    if 15 >= x + 4 >= 0 and 15 >= y + 1 >= 0:
        display.unicornhathd.set_pixel(x + 4, y + 1, 112, 32, 0)
    if 15 >= x + 4 >= 0 and 15 >= y + 2 >= 0:
        display.unicornhathd.set_pixel(x + 4, y + 2, 32, 8, 0)


def draw_wheel(x):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(14, x, wheel_color[0], wheel_color[1], wheel_color[2])
    if 15 >= x + 1 >= 0:
        display.unicornhathd.set_pixel(14, x + 1, wheel_color[0], wheel_color[1], wheel_color[2])


def draw_cab(x, light):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(13, x, 255, light, light)
        display.unicornhathd.set_pixel(12, x, train_color[0], train_color[1], train_color[2])


def connection(x):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(13, x, train_color[0], train_color[1], train_color[2])
        display.unicornhathd.set_pixel(12, x, train_color[0], train_color[1], train_color[2])
        display.unicornhathd.set_pixel(11, x, train_color[0] - 20, train_color[1], train_color[2] - 40)


def draw_window(x):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(13, x, train_color[0], train_color[1], train_color[2])
        display.unicornhathd.set_pixel(12, x, window_color[0], window_color[1], window_color[2])
        display.unicornhathd.set_pixel(11, x, train_color[0], train_color[1], train_color[2])


def draw_wall(x):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(13, x, train_color[0], train_color[1], train_color[2])
        display.unicornhathd.set_pixel(12, x, train_color[0], train_color[1], train_color[2])
        display.unicornhathd.set_pixel(11, x, train_color[0], train_color[1], train_color[2])


def draw_door(x):
    if 15 >= x >= 0:
        display.unicornhathd.set_pixel(13, x, door_colour[0], door_colour[1], door_colour[2])
        display.unicornhathd.set_pixel(12, x, door_colour[0], door_colour[1], door_colour[2])
        display.unicornhathd.set_pixel(11, x, train_color[0], train_color[1], train_color[2])


def draw_light(R, G):
    display.unicornhathd.set_pixel(14, 12, 16, 16, 16)
    display.unicornhathd.set_pixel(13, 12, 16, 16, 16)
    display.unicornhathd.set_pixel(12, 12, 16, 16, 16)
    display.unicornhathd.set_pixel(11, 12, R, G, 0)


def draw_carriage(start_x):
    draw_wall(start_x)
    draw_door(start_x + 1)
    draw_wall(start_x + 2)
    draw_window(start_x + 3)
    draw_wall(start_x + 4)
    draw_window(start_x + 5)
    draw_wall(start_x + 6)
    draw_door(start_x + 7)
    draw_wall(start_x + 8)
    draw_wheel(start_x + 1)
    draw_wheel(start_x + 6)


def draw_end_train(start_pixel, front_left: bool):
    if front_left:
        draw_wall(start_pixel)
    else:
        draw_cab(start_pixel, 0)
    draw_window(start_pixel + 1)
    draw_wall(start_pixel + 2)
    draw_window(start_pixel + 3)
    draw_wall(start_pixel + 4)
    draw_window(start_pixel + 5)
    draw_wall(start_pixel + 6)
    draw_window(start_pixel + 7)
    if front_left:
        draw_cab(start_pixel + 8, 255)
    else:
        draw_wall(start_pixel + 8)

    draw_wheel(start_pixel + 1)
    draw_wheel(start_pixel + 6)


def draw(start_pixel):
    display.unicornhathd.clear()
    draw_background()
    draw_light(0, 255)
    formation(start_pixel)
    display.unicornhathd.show()
    time.sleep(0.02)


def formation(starting_pixel):
    draw_end_train(starting_pixel, False)
    connection(starting_pixel + 9)
    draw_carriage(starting_pixel + 10)
    connection(starting_pixel + 19)
    draw_carriage(starting_pixel + 20)
    connection(starting_pixel + 29)
    draw_end_train(starting_pixel + 30, True)


def draw_background():
    draw_grass()
    draw_stars()
    draw_moon()


def animate_background_for(times):
    for _ in range(0, times):
        draw_background()
        display.unicornhathd.show()
        time.sleep(0.02)


def run_night_train():
    display.unicornhathd.brightness(0.4)
    draw_background()
    draw_light(255, 0)
    display.unicornhathd.show()
    animate_background_for(50)

    draw_light(224, 64)
    display.unicornhathd.show()
    animate_background_for(50)

    draw_light(0, 255)
    display.unicornhathd.show()
    animate_background_for(100)

    for start_pixel in range(-40, 40):
        draw(start_pixel)
    draw_light(255, 0)
    display.unicornhathd.show()
    animate_background_for(randint(20, 220))


if __name__ == '__main__':
    while True:
        run_night_train()
