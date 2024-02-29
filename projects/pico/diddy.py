"""
DIDdy Dom's information display


WIFI_CONFIG.py - can be found in dev drive
"""
import gc
import random
import WIFI_CONFIG
import uasyncio
import ujson
from urllib import urequest
from network_manager import NetworkManager
from pimoroni import ShiftRegister
from picographics import PicoGraphics, DISPLAY_INKY_FRAME
from machine import Pin
import machine

quotes = [
    [
        "It is so easy to say;;'You will do it tomorrow';;Re-program yourself to say:;;'Tomorrow is not a viable option.;;'You do it TODAY!'"],
    [
        "Pushing through difficulties;;  and struggles is a skill.;;You develop this skill;;  by doing it.;;If is easy,;; then is NOT worth doing."],
    ["Get things done;;through discipline.;;It must be an obsession;;because nothing beats hard work;;to achieve it."],
    [
        "Set your goal and go after it.;;You can achieve big goals;;  through 1000s little steps;;  using routine;;  because excellence comes;;from repetition.;;You must be insane to your craftsmanship."],
    [
        "It is OK to fail;;It is NOT OK;;  to not learn from mistakes.;;The best thing you can do;;  is take a lesson from the past;;  into the future.;;It is always better to learn;;  from others mistakes,;;  not yours."],
    ["Visualize good things;;  in times of struggle."],
    [
        "In your life,;;You will have turn back moment.;;You can go forward,;;  or you can give up.;;Keep in mind;;  that the guarantee of quitting;;  is that it will never happen.;;The only way,the possibility,;;  remains if you never give up.;;No matter what.;;The bottom line is;;  no matter what happens to you,;;  you got to keep going"],
    ["Make today;;  better than yesterday."],
    ["Eliminate things;;  and interactions;;  that made you sad."],
    [
        "Try to make the world;;  a better place;;  in your own way.;;If others disagree, that's OK.;;They can make the world;;  a better place in the own way."],
    ["Always try;;  to be as honest;;  but remember about;;  empathy when you speak."],
    ["Be humble.;;Gratitude is about;;  recognizing goodness;;  outside of ourselves."],
    ["Be happy from little things"]
]

# Setup Inky
ON = 1
OFF = 0
URL = 'http://192.168.0.200:5000/now-next'
URL_TODAY = 'http://192.168.0.200:5000/calendar/today'
DENVA_URL = 'http://192.168.0.201:5000/now'
DENVA_TWO_URL = 'http://192.168.0.205:5000/now'
# COLOURS
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
TAUPE = 7


def status_handler(mode, status, ip):
    print(mode, status, ip)


network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)

gc.collect()

display = PicoGraphics(display=DISPLAY_INKY_FRAME)
display.set_font("bitmap8")

led = Pin(6, Pin.OUT)
led.value(ON)

connectivity_led = Pin(7, Pin.OUT)

button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)

SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10

INIT_COUNTDOWN = 5000
sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)
sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / (65535)


def leds_off():
    button_a_led.off()
    button_b_led.off()
    button_c_led.off()
    button_d_led.off()
    button_e_led.off()
    led.value(OFF)
    connectivity_led.off()


def clear_display():
    display.set_pen(1)
    display.clear()


# set up
clear_display()
leds_off()

countdown = INIT_COUNTDOWN
choice = 0

def display_today():
    clear_display()
    try:
        connectivity_led.on()
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        socket = urequest.urlopen(URL)
        daily_routine = ujson.load(socket)
        connectivity_led.off()
        event_now = daily_routine['now']
        event_next = daily_routine['next']
        celebration = daily_routine['celebration']
        socket.close()
        display.set_pen(BLACK)
        display.text("Daily Routine", 10, 10, scale=6)
        display.text("Now:", 10, 70, scale=5)
        display.text(event_now, 10, 110, scale=3)
        display.text("Next:", 10, 150, scale=5)
        display.text(event_next, 10, 200, scale=3)
        display.text("Celebration:", 10, 240, scale=5)
        display.text(celebration, 10, 290, scale=3)
        display.update()
    except Exception as exception:
        display.set_pen(RED)
        display.text("ERROR", 10, 10, scale=6)
        display.text(str(exception), 10, 40, scale=2)
        display.update()

def display_calendar():
    clear_display()
    try:
        connectivity_led.on()
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        socket = urequest.urlopen(URL)
        daily_routine = ujson.load(socket)
        connectivity_led.off()
        event_now = daily_routine['now']
        event_next = daily_routine['next']
        celebration = daily_routine['celebration']
        socket.close()
        display.set_pen(BLACK)
        display.text("Daily Routine", 10, 10, scale=6)
        display.text("Now:", 10, 70, scale=5)
        display.text(event_now, 10, 110, scale=3)
        display.text("Next:", 10, 150, scale=5)
        display.text(event_next, 10, 200, scale=3)
        display.text("Celebration:", 10, 240, scale=5)
        display.text(celebration, 10, 290, scale=3)
        display.update()
    except Exception as exception:
        display.set_pen(RED)
        display.text("ERROR", 10, 10, scale=6)
        display.text(str(exception), 10, 40, scale=2)
        display.update()


def display_pico_status():
    clear_display()
    display.set_pen(BLUE)
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    cpu_speed = (machine.freq()/1000000)
    mem_free_value = gc.mem_free()
    display.text(f"Pico Temp: {temperature:.2f}°C ", 10, 10, scale=3)
    display.text(f"Pico Cpu speed: {cpu_speed:.1f}Mhz ", 10, 40, scale=3)
    display.text(f"Pico Memory Available: {mem_free_value} bytes", 10, 70, scale=3)
    display.update()

display_pico_status()

def display_quotes():
    clear_display()
    display.set_pen(GREEN)
    v = 10
    quote_number = random.randint(0, len(quotes) - 1)
    quote = quotes[quote_number]
    quote = quote[0].split(';;')
    for sentence in quote:
        display.text(sentence, 10, v, scale=4)
        v += 32
    display.update()


while True:

    # check if button was pressed
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]

    if button_a == 1:  # Auto
        button_a_led.on()
        print('Button A pressed')
        button_a_led.off()
    elif button_b == 1:
        button_b_led.on()
        print('Button B pressed')
        display_quotes()
        button_b_led.off()
    elif button_c == 1:
        button_c_led.on()
        display.set_pen(YELLOW)
        display.text("Button C pressed", 10, 10, scale=3)
        display.update()
        button_c_led.off()
    elif button_d == 1:
        button_d_led.on()
        print('Button D pressed')
        display_pico_status()
        button_d_led.off()
    elif button_e == 1:
        button_e_led.on()
        display_calendar()
        button_e_led.off()

    if countdown <= 0:
        led.value(ON)
        if choice == 0:
            display_pico_status()
        elif choice == 1:
            display_calendar()
        elif choice == 2:
            display_quotes()

        choice += 1
        if choice > 2:
            choice = 0
        countdown = INIT_COUNTDOWN
        led.value(OFF)
    else:
        countdown -= 1

    print(countdown)
    gc.collect()
