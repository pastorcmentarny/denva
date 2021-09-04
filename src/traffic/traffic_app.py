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


all_red()


def opposite_sides(first_red: PiTraffic.Traffic, first_yellow: PiTraffic.Traffic, first_green: PiTraffic.Traffic,
                   second_red: PiTraffic.Traffic, second_yellow: PiTraffic.Traffic, second_green: PiTraffic.Traffic):
    first_red.off()
    second_red.off()
    first_yellow.on()
    second_yellow.on()
    time.sleep(1)
    first_yellow.off()
    second_yellow.off()
    first_green.on()
    second_green.on()
    time.sleep(random.randint(1, 5))
    first_green.off()
    second_green.off()
    for _ in range(0, 3):
        first_yellow.on()
        second_yellow.on()
        time.sleep(0.25)
        first_yellow.off()
        second_yellow.off()
        time.sleep(0.25)
    first_red.on()
    second_red.on()
    time.sleep(1)
    return ''


def traffic_cycle(red: PiTraffic.Traffic, yellow: PiTraffic.Traffic, green: PiTraffic.Traffic):
    red.off()
    yellow.on()
    time.sleep(1)
    yellow.off()
    green.on()
    time.sleep(random.randint(1, 5))
    green.off()
    for _ in range(0, 3):
        yellow.on()
        time.sleep(0.25)
        yellow.off()
        time.sleep(0.25)
    red.on()
    time.sleep(1)
    return ''


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
        counter += 1

        #       Buzz.on()
        #       time.sleep(0.2)
        #       Buzz.off()
        choice = random.randint(0, 6)
        print(choice)
        print(traffic_options[choice])

        off()
        all_red()



except KeyboardInterrupt:
    PiTraffic.closeGPIO()