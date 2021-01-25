import random

import numpy

scale = 3

p = 0.01
f = 0.0005

forest_height = 0
forest_width = 0

hood_size = 3
avg_size = scale

tree = [0, 255, 0]
start_burning = [235, 101, 0]
burning = [255, 0, 0]
space = [0, 0, 0]

trees = [[160, 32, 240], [0, 255, 0], [255, 255, 255]]
start_burning_trees = [[112, 26, 180], [235, 101, 0], [128, 128, 128]]
burning_colour = [[255, 110, 0], [255, 0, 0], [48, 48, 48]]


def in_the_forest(unicornhathd):
    global forest_height
    global forest_width
    width, height = unicornhathd.get_shape()
    forest_width = width * scale
    forest_height = height * scale
    forest = initialise_forest()
    burnt = True
    while burnt:
        show_forest(forest, unicornhathd, width, height)
        forest = update_forest(forest)
        burnt = quit_if_burnt(forest)


def show_forest(forest, unicornhathd, width, height):
    avg_forest = average_forest(forest, width, height)

    for x in range(width):
        for y in range(height):
            red, green, blue = avg_forest[x][y]
            unicornhathd.set_pixel(x, y, int(red), int(green), int(blue))

    unicornhathd.show()


def initialise_forest():
    global tree
    global burning
    global start_burning
    idx = random.randint(0, 2)
    tree = trees[idx]
    start_burning = start_burning_trees[idx]
    burning = burning_colour[idx]
    initial_trees = 0.55
    forest = [[tree if random.random() <= initial_trees else space for _ in range(forest_width)] for _ in
              range(forest_height)]
    return forest


def update_forest(forest):
    new_forest = [[space for _ in range(forest_width)] for _ in range(forest_height)]  # FIXME REMOVE IT?
    for width in range(forest_width):
        for height in range(forest_height):
            if forest[width][height] == start_burning:
                new_forest[width][height] = burning
            elif forest[width][height] == burning:
                new_forest[width][height] = space
            elif forest[width][height] == tree:
                neighbours = get_neighbours(width, height, hood_size)
                new_forest[width][height] = (burning if any(
                    [forest[n[0]][n[1]] == burning for n in
                     neighbours]) or random.random() <= f else tree)  # TODO change it
    return new_forest


def quit_if_burnt(forest):
    for width in range(forest_width):
        for height in range(forest_height):
            if forest[width][height] != space:
                return True  # it still burning
    return False


def average_forest(forest, width, height):
    avg_forest = [[space for _ in range(width)] for _ in range(height)]

    for i, x in enumerate(range(1, forest_width, scale)):
        for j, y in enumerate(range(1, forest_height, scale)):
            neighbours = get_neighbours(x, y, avg_size)
            red = int(numpy.mean([forest[n[0]][n[1]][0] for n in neighbours]))
            green = int(numpy.mean([forest[n[0]][n[1]][1] for n in neighbours]))
            blue = int(numpy.mean([forest[n[0]][n[1]][2] for n in neighbours]))
            avg_forest[i][j] = [red, green, blue]

    return avg_forest


def get_neighbours(x, y, z):
    return [(x2, y2) for x2 in range(x - (z - 1), x + z) for y2 in range(y - (z - 1), y + z) if (
            -1 < x < forest_width and -1 < y < forest_height and (x != x2 or y != y2) and (
            0 <= x2 < forest_width) and (0 <= y2 < forest_height))]
