import random

import time

import PiTraffic

SouthRed = PiTraffic.Traffic("SOUTH", "RED")
SouthYellow = PiTraffic.Traffic("SOUTH", "YELLOW")
SouthGreen = PiTraffic.Traffic("SOUTH", "GREEN")

EastRed = PiTraffic.Traffic("EAST", "RED")
EastYellow = PiTraffic.Traffic("EAST", "YELLOW")
EastGreen = PiTraffic.Traffic("EAST", "GREEN")

NorthRed = PiTraffic.Traffic("NORTH", "RED")
NorthYellow = PiTraffic.Traffic("NORTH", "YELLOW")
NorthGreen = PiTraffic.Traffic("NORTH", "GREEN")

WestRed = PiTraffic.Traffic("WEST", "RED")
WestYellow = PiTraffic.Traffic("WEST", "YELLOW")
WestGreen = PiTraffic.Traffic("WEST", "GREEN")

Buzz = PiTraffic.Buzzer()


def all_red():
    SouthRed.on()
    EastRed.on()
    NorthRed.on()
    WestRed.on()


def blinking_yellow():
    off()
    repeats = random.randint(2, 10) * 4
    for _ in range(0, repeats):
        WestYellow.on()
        NorthYellow.on()
        EastYellow.on()
        SouthYellow.on()
        time.sleep(0.25)
        WestYellow.off()
        NorthYellow.off()
        EastYellow.off()
        SouthYellow.off()
        time.sleep(0.25)
    off()
    all_red()


def off():
    SouthRed.off()
    EastRed.off()
    NorthRed.off()
    WestRed.off()
    SouthYellow.off()
    EastYellow.off()
    NorthYellow.off()
    WestYellow.off()
    SouthGreen.off()
    EastGreen.off()
    NorthGreen.off()
    WestGreen.off()


# not in use now, but to use later
def play_sound():
    Buzz.on()
    time.sleep(0.2)
    Buzz.off()


all_red()


def opposite_sides(first_red: PiTraffic.Traffic, first_yellow: PiTraffic.Traffic, first_green: PiTraffic.Traffic,
                   second_red: PiTraffic.Traffic, second_yellow: PiTraffic.Traffic, second_green: PiTraffic.Traffic):
    first_red.on()
    second_red.on()
    first_yellow.on()
    second_yellow.on()
    time.sleep(1)
    first_red.off()
    second_red.off()
    first_yellow.off()
    second_yellow.off()
    first_green.on()
    second_green.on()
    time.sleep(random.randint(1, 10))
    first_green.off()
    second_green.off()
    first_yellow.on()
    second_yellow.on()
    time.sleep(2)
    first_red.on()
    second_red.on()
    time.sleep(1)
    return ''


def traffic_cycle(red: PiTraffic.Traffic, yellow: PiTraffic.Traffic, green: PiTraffic.Traffic):
    red.on()
    yellow.on()
    time.sleep(1)
    red.off()
    yellow.off()
    green.on()
    time.sleep(random.randint(1, 6))
    green.off()
    yellow.on()
    time.sleep(random.randint(1, 3))
    red.on()
    time.sleep(1)
    return ''


# do not work
traffic_options = {
    0: traffic_cycle(NorthRed, NorthYellow, NorthGreen),
    1: traffic_cycle(EastRed, EastYellow, EastGreen),
    2: traffic_cycle(SouthRed, SouthYellow, SouthGreen),
    3: traffic_cycle(WestRed, WestYellow, WestGreen),
    4: opposite_sides(WestRed, WestYellow, WestGreen, EastRed, EastYellow, EastGreen),
    5: opposite_sides(NorthRed, NorthYellow, NorthGreen, SouthRed, SouthYellow, SouthGreen),
    6: all_red()
}

try:
    counter = 0
    while True:
        print(f'cycle: {counter}')
        if counter % 13 == 0:
            blinking_yellow()
        choice = random.randint(0, 6)
        if choice == 0:
            traffic_cycle(NorthRed, NorthYellow, NorthGreen)
        if choice == 1:
            traffic_cycle(EastRed, EastYellow, EastGreen)
        if choice == 2:
            traffic_cycle(SouthRed, SouthYellow, SouthGreen)
        if choice == 3:
            traffic_cycle(WestRed, WestYellow, WestGreen)
        if choice == 4:
            opposite_sides(WestRed, WestYellow, WestGreen, EastRed, EastYellow, EastGreen)
        if choice == 5:
            opposite_sides(NorthRed, NorthYellow, NorthGreen, SouthRed, SouthYellow, SouthGreen)
        if choice == 6:
            all_red()
            time.sleep(random.randint(1, 6))
        all_red()
        time.sleep(random.randint(1, 3))
        counter += 1

except KeyboardInterrupt:
    PiTraffic.closeGPIO()
