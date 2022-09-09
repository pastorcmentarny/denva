import gc
import random
from pimoroni import ShiftRegister
from picographics import PicoGraphics, DISPLAY_INKY_FRAME
from machine import Pin

quotes = [
    ["It is so easy to say;;'You will do it tomorrow';;Re-program yourself to say:;;'Tomorrow is not a viable option.;;'You do it TODAY!'"],
    ["Pushing through difficulties;;  and struggles is a skill.;;You develop this skill;;  by doing it.;;If is easy,;; then is NOT worth doing."],
    ["Get things done;;through discipline.;;It must be an obsession;;because nothing beats hard work;;to achieve it."],
    ["Set your goal and go after it.;;You can achieve big goals;;  through 1000s little steps;;  using routine;;  because excellence comes;;from repetition.;;You must be insane to your craftsmanship."],
    ["It is OK to fail;;It is NOT OK;;  to not learn from mistakes.;;The best thing you can do;;  is take a lesson from the past;;  into the future.;;It is always better to learn;;  from others mistakes,;;  not yours."],
    ["Visualize good things;;  in times of struggle."],
    ["In your life,;;You will have turn back moment.;;You can go forward,;;  or you can give up.;;Keep in mind;;  that the guarantee of quitting;;  is that it will never happen.;;The only way,the possibility,;;  remains if you never give up.;;No matter what."],
    ["Make today;;  better than yesterday."],
    ["Eliminate things;;  and interactions;;  that made you sad."],
    ["Try to make the world;;  a better place;;  in your own way.;;If others disagree, that's OK.;;They can make the world;;  a better place in the own way."],
    ["Always try;;  to be as honest;;  but remember about;;  empathy when you speak."],
    ["Be humble.;;Gratitude is about;;  recognizing goodness;;  outside of ourselves."],
    ["Be happy from little things"]
]


#Setup Inky
display = PicoGraphics(display=DISPLAY_INKY_FRAME)
display.set_font("bitmap8")


SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10

sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)

button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)


def clear():
    display.set_pen(1)
    display.clear()


# set up
clear()
display.set_pen(0)
display.text("#. Dom's status display", 10, 10, scale=4)
display.text("1. Denva", 10, 43, scale=4)
display.text("2. Enviro", 10, 77, scale=4)
display.text("3. Quotes", 10, 110, scale=4)
display.text("4. Information", 10, 143, scale=4)
display.text("5. Daily routine", 10, 176, scale=4)
display.update()
gc.collect()


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

    if button_a == 1: # Auto
        button_a_led.on()
        clear()
        display.set_pen(4)
        display.text("It is so easy to say", 10, 10, scale=4)
        display.text('You will do it tomorrow', 20, 42, scale=4)
        display.text('Re-program yourself to say', 10, 74, scale=4)
        display.text('Tomorrow is not a viable option', 10, 106, scale=4)
        display.text('You do it TODAY!', 10, 138, scale=4)
        display.update()
    elif button_b == 1:
        button_d_led.on()
        clear()
        display.set_pen(6)
        display.text("Button B pressed", 10, 130, scale=4)
        display.update()
    elif button_c == 1: # Quotes
        button_c_led.on()
        clear()
        display.set_pen(4)
        v = 10
        quote_number = random.randint(0, len(quotes)-1)
        quote = quotes[quote_number]
        quote = quote[0].split(';;')
        for sentence in quote:
            display.text(sentence, 10, v, scale=4)
            v+=32
        display.update()
    elif button_d == 1:
        button_d_led.on()
        clear()
        display.set_pen(2)
        display.text("Button D pressed", 10, 130, scale=4)
        display.update()
    elif button_e == 1:
        button_e_led.on()
        clear()
        pen_type = 1
        display.set_pen(1)
        display.text("Button E pressed", 10, 130, scale=4)
        display.update()