import time
from random import randint

import unicornhathd

unicornhathd.brightness(0.5)

counter = 0
for x in range(0, 16):
    for y in range(0, 16):
        unicornhathd.set_pixel(x, y, randint(0, 255), randint(0, 255), randint(0, 255))
        unicornhathd.show()
time.sleep(1)

while True:
    if counter % 100 == 0:
        print(f'counter:{counter}')
    unicornhathd.set_pixel(randint(0, 15), randint(0, 15), randint(0, 255), randint(0, 255), randint(0, 255))
    unicornhathd.show()
    time.sleep(0.01)
    counter += 1