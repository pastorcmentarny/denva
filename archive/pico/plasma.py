import plasma
from plasma import plasma_stick
import time
import random
from machine import Pin

# Set how many LEDs you have
NUM_LEDS = 16


# Set up brightness (between 0 and 1)
BRIGHTNESS = 0.2

# Set up speed (wait time between colour changes, in seconds)
SPEED = 0.2

# set up the Pico W's onboard LED
pico_led = Pin('LED', Pin.OUT)


# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# Start updating the LED strip
led_strip.start()

while True:
    for i in range(NUM_LEDS):
        if random.randint(1, 100) > 20:
            led_strip.set_hsv(i, random.randint(76, 87)/ 360, 0.9, random.uniform(0.2, 0.4))
    time.sleep(random.uniform(0.02, 0.2))


