# Run on Galactic Unicorn (Pico)

import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import random

RUISLIP_MANOR = 'Ruislip Manor'
RUISLIP = 'Ruislip'
ICKENHAM = 'Ickenham'
HILLINGDON = 'Hillingdon'
EASTCOTE = 'Eastcote'
CROXLEY = 'Croxley'
WEST_HARROW = 'West Harrow'
CHORLEYWOOD = 'Chorleywood'
RICKMANSWORTH = 'Rickmansworth'
CHALFONT_LATIMER = 'Chalfont & Latimer'
MOOR_PARK = 'Moor Park'
NORTHWOOD = 'Northwood'
NORTHWOOD_HILLS = 'Northwood Hills'
PINNER = 'Pinner'
NORTH_HARROW = 'North Harrow'
UXBRIDGE = 'Uxbridge'
WATFORD = 'Watford'
AMERSHAM = 'Amersham'
CHESHAM = 'Chesham'
HOH = 'Harrow-on-the-Hill'

# constants for controlling scrolling text
PADDING = 5
MESSAGE_COLOUR = (220, 132, 0)
OUTLINE_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (0, 0, 0)
# MESSAGE = "This is a semi-fast Metropolitan line service to Amersham.The next station is Rickmansworth.The service is from Aldgate. Calling at: Rickmansworth, Chorleywood, Chalfont & Latimer and Amersham."
# MESSAGE = "This is a semi-fast Metropolitan line service to Amersham.The next station is Rickmansworth.The service is from Aldgate. Calling at: Liverpool Street, Moorgate, Barbican, Farringdon, King's Cross St. Pancras, Euston Square, Great Portland Street, Baker Street, Finchley Road, Wembley Park, Preston Road, Northwick Park, Harrow-on-the-Hill, North Harrow, Pinner, Northwood Hills, Northwood, Moor Park, Rickmansworth, Chorleywood, Chalfont & Latimer and Amersham."
# MESSAGE = "Platform 6 , for the 12:00 service to Aylesbury Vale Parkway. Calling at: Rickmansworth, Chorleywood, Amersham , Great Missenden, Wendover, Stoke Mandeville, Aylesbury and Aylesbury Vale Parkway.This train si formed of 6 carriages."
# MESSAGE = "I love trains, this train is going to aylesubry and Aylesbury Vale Parkway. Calling at: Rickmansworth, Chorleywood, Amersham , Great Missenden, Wendover, Stoke Mandeville, Aylesbury and Aylesbury Vale Parkway.This train si formed of 6 carriages."
HOLD_TIME = 0.5
STEP_TIME = 0.001

# create galactic object and graphics surface for drawing
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

stopping_pattern = ['all stations', 'semi-fast', 'fast']
destination = [AMERSHAM, CHESHAM, WATFORD, UXBRIDGE, 'Baker Street', 'Aldgate']
all_stations = ['Aldgate', AMERSHAM, 'Baker Street', 'Barbican', CHALFONT_LATIMER, CHESHAM, CHORLEYWOOD,
                CROXLEY, EASTCOTE, 'Euston Square', 'Farringdon', 'Great Portland Street', HOH,
                HILLINGDON, ICKENHAM, 'King\'s Cross St. Pancras', 'Liverpool Street', MOOR_PARK, NORTH_HARROW,
                'Northwick Park', NORTHWOOD, NORTHWOOD_HILLS, PINNER, 'Preston Road', 'Rayners Lane',
                RICKMANSWORTH, RUISLIP, RUISLIP_MANOR, UXBRIDGE, WATFORD, 'Wembley Park', WEST_HARROW]

next_station = ['Aldgate', AMERSHAM, 'Baker Street', 'Barbican', CHALFONT_LATIMER, CHESHAM, CHORLEYWOOD,
                CROXLEY, EASTCOTE, 'Euston Square', 'Farringdon', 'Great Portland Street', HOH,
                HILLINGDON, ICKENHAM, 'King\'s Cross St. Pancras', 'Liverpool Street', MOOR_PARK, NORTH_HARROW,
                'Northwick Park', NORTHWOOD, NORTHWOOD_HILLS, PINNER, 'Preston Road', 'Rayners Lane',
                RICKMANSWORTH, RUISLIP, RUISLIP_MANOR, UXBRIDGE, WATFORD, 'Wembley Park', WEST_HARROW]


def remove_impossible_routes_for(selected_destination):
    if selected_destination == AMERSHAM:
        next_station.remove(CHESHAM)
        next_station.remove(WEST_HARROW)
        next_station.remove(EASTCOTE)
        next_station.remove(HILLINGDON)
        next_station.remove(ICKENHAM)
        next_station.remove(RUISLIP)
        next_station.remove(RUISLIP_MANOR)
        next_station.remove(UXBRIDGE)
    elif selected_destination == CHESHAM:
        next_station.remove(AMERSHAM)
        next_station.remove(WEST_HARROW)
        next_station.remove(EASTCOTE)
        next_station.remove(HILLINGDON)
        next_station.remove(ICKENHAM)
        next_station.remove(RUISLIP)
        next_station.remove(RUISLIP_MANOR)
        next_station.remove(UXBRIDGE)
    elif selected_destination == WATFORD:
        next_station.remove(WEST_HARROW)
        next_station.remove(EASTCOTE)
        next_station.remove(HILLINGDON)
        next_station.remove(ICKENHAM)
        next_station.remove(RUISLIP)
        next_station.remove(RUISLIP_MANOR)
        next_station.remove(UXBRIDGE)
    elif selected_destination == UXBRIDGE:
        next_station.remove(NORTH_HARROW)
        next_station.remove(PINNER)
        next_station.remove(NORTHWOOD)
        next_station.remove(NORTHWOOD_HILLS)
        next_station.remove(MOOR_PARK)
        next_station.remove(CROXLEY)
        next_station.remove(WATFORD)
        next_station.remove(RICKMANSWORTH)
        next_station.remove(CHORLEYWOOD)
        next_station.remove(CHALFONT_LATIMER)
        next_station.remove(AMERSHAM)
        next_station.remove(CHESHAM)


def get_stopping_pattern_type():
    return stopping_pattern[random.randint(0, len(stopping_pattern) - 1)]


def get_destination():
    return destination[random.randint(0, len(destination) - 1)]


def get_random_station():
    return next_station[random.randint(0, len(next_station) - 1)]


def add_randomly_mind_the_gap():
    if bool(random.getrandbits(1)):
        return ' Mind the gap between the train and the platform.'
    return ''


def add_terminates_message(next_station: str, destination: str) -> str:
    if (next_station == destination) and (next_station in destination):
        return 'where this train terminates. Please take all belongings with you when you leave the train.'
    return '.'


def add_rear_door_not_open_this(selected_station):
    if selected_station in ['Barbican', 'Great Portland Street']:
        return ' The rear door will not open here.Please use other doors.'
    return ''


def add_rear_door_not_open_next(selected_station):
    if selected_station in ['Barbican', 'Great Portland Street']:
        return ' The rear door will not open at the next station.Please use other doors.'
    return ''


def generate() -> str:
    selected_stopping_pattern = get_stopping_pattern_type()
    selected_destination = get_destination()
    remove_impossible_routes_for(selected_destination)
    selected_station = get_random_station()
    return f'This is {selected_stopping_pattern} Metropolitan line service to {selected_destination}. The next station is {selected_station}{add_terminates_message(selected_station, selected_destination)}{add_rear_door_not_open_next(selected_station)}{add_randomly_mind_the_gap()}'


'''
Display scrolling wisdom, quotes or greetz.
You can adjust the brightness with LUX + and -.
'''


# function for drawing outlined text
def outline_text(text, x, y):
    graphics.set_pen(graphics.create_pen(int(OUTLINE_COLOUR[0]), int(OUTLINE_COLOUR[1]), int(OUTLINE_COLOUR[2])))
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
    graphics.text(text, x, y, -1, 1)


gu.set_brightness(0.4)

MESSAGE = generate()
# state constants
STATE_PRE_SCROLL = 0
STATE_SCROLLING = 1
STATE_POST_SCROLL = 2
MULTIPLIER = 1000

shift = 0
state = STATE_PRE_SCROLL

# set the font
graphics.set_font("bitmap8")

# calculate the message width so scrolling can happen
msg_width = graphics.measure_text(MESSAGE, 1)

last_time = time.ticks_ms()

while True:
    time_ms = time.ticks_ms()

    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        gu.adjust_brightness(+0.01)

    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        gu.adjust_brightness(-0.01)

    if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * MULTIPLIER:
        if msg_width + PADDING * 2 >= width:
            state = STATE_SCROLLING
        last_time = time_ms

    if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * MULTIPLIER:
        shift += 1
        if shift >= (msg_width + PADDING * 2) - width - 1:
            state = STATE_POST_SCROLL
        last_time = time_ms

    if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * MULTIPLIER:
        state = STATE_PRE_SCROLL
        shift = 0
        MESSAGE = generate()
        next_station.clear()
        next_station = all_stations.copy()
        msg_width = graphics.measure_text(MESSAGE, 1)
        last_time = time_ms

    graphics.set_pen(
        graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
    graphics.clear_display()

    outline_text(MESSAGE, x=PADDING - shift, y=2)

    # update the display
    gu.update(graphics)

    # pause for a moment (important or the USB serial device will fail)
    time.sleep(0.001)
