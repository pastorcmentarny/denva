require "keybow"
require "snippets/win_snippets"

function setup()
    keybow.auto_lights(false)
    keybow.clear_lights()
    keybow.set_pixel(0, 192, 64, 0)
    keybow.set_pixel(1, 192, 64, 0)
    keybow.set_pixel(2, 192, 64, 0)
    keybow.set_pixel(3, 192, 64, 0)
    keybow.set_pixel(4, 192, 64, 0)
    keybow.set_pixel(5, 192, 64, 0)
    keybow.set_pixel(6, 159, 255, 47)
    keybow.set_pixel(7, 75, 0, 130)
    keybow.set_pixel(8, 128, 0, 128)
    keybow.set_pixel(9, 64, 64, 64)
    keybow.set_pixel(10, 128, 128, 0)
    keybow.set_pixel(11, 128, 0, 0)
end


--- keyboard light  on
function handle_key_00(pressed)
    for index = 1, 10 do
        keybow.sleep(200)
        keybow.set_pixel(0, 255, 255, 255)
        keybow.sleep(200)
        keybow.set_pixel(0, 192, 64, 0)
    end

    keybow.set_pixel(0, 192, 64, 0)
    keybow.set_pixel(1, 192, 64, 0)
    keybow.set_pixel(2, 192, 64, 0)
    keybow.set_pixel(3, 192, 64, 0)
    keybow.set_pixel(4, 192, 64, 0)
    keybow.set_pixel(5, 192, 64, 0)
    keybow.set_pixel(6, 159, 255, 47)
    keybow.set_pixel(7, 75, 0, 130)
    keybow.set_pixel(8, 128, 0, 128)
    keybow.set_pixel(9, 64, 64, 64)
    keybow.set_pixel(10, 128, 128, 0)
    keybow.set_pixel(11, 128, 0, 0)
end


--- keyboard light off
function handle_key_01(pressed)
    for index = 1, 11 do
        keybow.set_pixel(index, 0, 0, 0)
    end

    for index = 1, 10 do
        keybow.sleep(200)
        keybow.set_pixel(0, 0, 0, 0)
        keybow.sleep(200)
        keybow.set_pixel(0, 192, 64, 0)
    end

    keybow.sleep(200)
    keybow.set_pixel(0, 0, 0, 0)
    keybow.sleep(200)
    keybow.set_pixel(0, 128, 48, 0)
    keybow.sleep(200)
    keybow.set_pixel(0, 96, 32, 0)
    keybow.sleep(200)
    keybow.set_pixel(0, 64, 24, 0)
    keybow.sleep(200)
    keybow.set_pixel(0, 0, 0, 0)
end


--- status light on
function handle_key_02(pressed)
    keybow.set_pixel(2, 32, 32, 32)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.set_pixel(2, 64, 64, 64)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py light_off")
    keybow.sleep(100)
    keybow.set_pixel(2, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(2, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(2, 48, 48, 48)
    keybow.tap_enter()
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(100)
    keybow.set_pixel(2, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(2, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(2, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(2, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(2, 32, 32, 32)
end


--- fire with lighting
function handle_key_03(pressed)
    keybow.set_pixel(3, 32, 32, 32)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.set_pixel(3, 64, 64, 64)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py fire")
    keybow.sleep(100)
    keybow.set_pixel(3, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(3, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(3, 48, 48, 48)
    keybow.tap_enter()
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(100)
    keybow.set_pixel(3, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(3, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(3, 32, 32, 32)
    keybow.sleep(100)
    keybow.set_pixel(3, 64, 64, 64)
    keybow.sleep(100)
    keybow.set_pixel(3, 32, 32, 32)
end


function handle_key_04(pressed)
    keybow.set_key("3", pressed)
end


function handle_key_05(pressed)
    keybow.set_key("4", pressed)
end

--- borg mode
function handle_key_06(pressed)
    keybow.set_pixel(6, 32, 32, 32)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py borg")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(6, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(6, 159, 255, 47)
end

--- rain mode
function handle_key_07(pressed)
    keybow.set_pixel(7, 160, 202, 8)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py rain")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(7, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(7, 75, 0, 130)
end

-- dream mode
function handle_key_08(pressed)
    keybow.set_pixel(8, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py dream")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(8, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(8, 128, 0, 128)
end

-- daily routine mode
function handle_key_09(pressed)
    keybow.set_pixel(9, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(9, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(9, 64, 64, 64)
end

-- busy mode
function handle_key_10(pressed)
    keybow.set_pixel(10, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python  D:\\denva\\src\\overseer\\manual_status_override.py yellow")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(10, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(10, 128, 128, 0)
end

-- work mode
function handle_key_11(pressed)
    keybow.set_pixel(11, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python D:\\denva\\src\\overseer\\manual_status_override.py red")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(11, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(11, 128, 0, 0)
end
