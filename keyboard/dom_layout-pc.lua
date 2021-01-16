require "keybow"
require "snippets/win_snippets"

-- dev version for pc to test

function setup()
    -- Set custom lights up
    keybow.auto_lights(false)
    keybow.clear_lights()
    keybow.set_pixel(0, 192, 64, 0)
    keybow.set_pixel(1, 192, 64, 0)
    keybow.set_pixel(2, 255, 255, 0)
    keybow.set_pixel(3, 192, 64, 0)
    keybow.set_pixel(4, 192, 64, 0)
    keybow.set_pixel(5, 255, 255, 255)
    keybow.set_pixel(6, 192, 64, 0)
    keybow.set_pixel(7, 192, 64, 0)
    keybow.set_pixel(8, 128, 128, 128)
    keybow.set_pixel(9, 192, 64, 0)
    keybow.set_pixel(10, 192, 64, 0)
    keybow.set_pixel(11, 192, 64, 0)
end

function handle_key_02(pressed)
    keybow.set_pixel(2, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py dream")

    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(2, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(2, 128, 128, 0)
end

function handle_key_05(pressed)
    keybow.set_pixel(5, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py rain")

    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(5, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(5, 128, 128, 0)
end

function handle_key_08(pressed)
    keybow.set_pixel(8, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(8, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(8, 0, 0, 128)
end
