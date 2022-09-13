"""
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
    ["It is so easy to say;;'You will do it tomorrow';;Re-program yourself to say:;;'Tomorrow is not a viable option.;;'You do it TODAY!'"],
    ["Pushing through difficulties;;  and struggles is a skill.;;You develop this skill;;  by doing it.;;If is easy,;; then is NOT worth doing."],
    ["Get things done;;through discipline.;;It must be an obsession;;because nothing beats hard work;;to achieve it."],
    ["Set your goal and go after it.;;You can achieve big goals;;  through 1000s little steps;;  using routine;;  because excellence comes;;from repetition.;;You must be insane to your craftsmanship."],
    ["It is OK to fail;;It is NOT OK;;  to not learn from mistakes.;;The best thing you can do;;  is take a lesson from the past;;  into the future.;;It is always better to learn;;  from others mistakes,;;  not yours."],
    ["Visualize good things;;  in times of struggle."],
    ["In your life,;;You will have turn back moment.;;You can go forward,;;  or you can give up.;;Keep in mind;;  that the guarantee of quitting;;  is that it will never happen.;;The only way,the possibility,;;  remains if you never give up.;;No matter what.;;The bottom line is;;  no matter what happens to you,;;  you got to keep going"],
    ["Make today;;  better than yesterday."],
    ["Eliminate things;;  and interactions;;  that made you sad."],
    ["Try to make the world;;  a better place;;  in your own way.;;If others disagree, that's OK.;;They can make the world;;  a better place in the own way."],
    ["Always try;;  to be as honest;;  but remember about;;  empathy when you speak."],
    ["Be humble.;;Gratitude is about;;  recognizing goodness;;  outside of ourselves."],
    ["Be happy from little things"]
]

# Setup Inky
ON = 1
OFF = 0
URL = 'http://192.168.0.200:5000/now-next'
DENVA_URL = 'http://192.168.0.201:5000/now'
ENVIRO_URL = 'http://192.168.0.202:5000/now'
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

sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)
sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / (65535)


def clear():
    display.set_pen(1)
    display.clear()


# set up
clear()
display.set_pen(BLACK)
display.text("#. Dom's status display", 10, 10, scale=4)
display.text("1. Denva", 10, 43, scale=4)
display.text("2. Enviro", 10, 77, scale=4)
display.text("3. Quotes", 10, 110, scale=4)
display.text("4. Information", 10, 143, scale=4)
display.text("5. Daily routine", 10, 176, scale=4)
display.update()
gc.collect()
led.value(OFF)

while True:
    button_a_led.off()
    button_b_led.off()
    button_c_led.off()
    button_d_led.off()
    button_e_led.off()

    # read the shift register
    # we can tell which button has been pressed by checking if a specific bit is 0 or 1
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]

    if button_a == 1:  # Auto
        led.value(ON)
        button_a_led.on()
        clear()
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        socket = urequest.urlopen(DENVA_URL)
        denva_result = ujson.load(socket)
        temperature = denva_result['co2_temperature']
        humidity = denva_result["humidity"]
        pressure = denva_result["pressure"]
        co2 = denva_result['co2']
        eco2 = denva_result['eco2']
        tvoc = denva_result['tvoc']
        colour = denva_result['colour']
        socket.close()
        display.set_pen(BLACK)
        display.text("Denva", 10, 10, scale=5)
        display.text("Temp: " + temperature, 10, 60, scale=4)
        display.text("Humidity: " + humidity, 10, 93, scale=4)
        display.text("Pressure: " + pressure, 10, 126, scale=4)
        display.text("Co2: " + co2, 10, 159, scale=4)
        display.text("Eco2: " + eco2, 10, 192, scale=4)
        display.text("Tvoc: " + tvoc, 10, 225, scale=4)
        display.text("Colour: " + colour, 10, 258, scale=4)
        display.update()
        gc.collect()
        led.value(OFF)
    elif button_b == 1:
        led.value(ON)
        button_b_led.on()
        clear()
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        socket = urequest.urlopen(ENVIRO_URL)
        denva_result = ujson.load(socket)
        light = denva_result["light"]
        nh3 = denva_result["nh3"]
        oxidised = denva_result['oxidised']
        reduced = denva_result['reduced']
        pm1 = denva_result['pm1']
        pm25 = denva_result['pm25']
        pm10 = denva_result['pm10']
        socket.close()
        display.set_pen(BLACK)
        display.text("Enviro", 10, 10, scale=5)
        display.text("Light: " + light, 10, 60, scale=4)
        display.text("nh3: " + nh3, 10, 93, scale=4)
        display.text("oxidised: " + oxidised, 10, 126, scale=4)
        display.text("reduced: " + reduced, 10, 159, scale=4)
        display.text("pm1: " + pm1, 10, 192, scale=4)
        display.text("pm25: " + pm25, 10, 225, scale=4)
        display.text("pm10: " + pm10, 10, 258, scale=4)
        display.update()
        gc.collect()
        led.value(OFF)
    elif button_c == 1:  # Quotes
        led.value(ON)
        button_c_led.on()
        clear()
        display.set_pen(4)
        v = 10
        quote_number = random.randint(0, len(quotes) - 1)
        quote = quotes[quote_number]
        quote = quote[0].split(';;')
        for sentence in quote:
            display.text(sentence, 10, v, scale=4)
            v += 32
        display.update()
        gc.collect()
        led.value(OFF)
    elif button_d == 1:
        led.value(ON)
        button_d_led.on()
        clear()
        display.set_pen(2)
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 10, scale=1)
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 32, scale=2)
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 64, scale=3)
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 100, scale=4)
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 260, scale=5)
        display.text("Pico Temp: {:.2f}°C,".format(temperature), 10, 310, scale=6)
        display.update()
        gc.collect()
        led.value(OFF)
    elif button_e == 1:
        led.value(ON)
        button_e_led.on()
        clear()
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        socket = urequest.urlopen(URL)
        daily_routine = ujson.load(socket)
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
        gc.collect()
        led.value(OFF)
