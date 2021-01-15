require "keybow"
require "snippets/win_snippets"

function setup()
    -- Set custom lights up
    keybow.auto_lights(false)
    keybow.clear_lights()
    keybow.set_pixel(0, 192, 64, 0)
    keybow.set_pixel(1, 192, 64, 0)
    keybow.set_pixel(2, 192, 64, 0)
    keybow.set_pixel(3, 192, 64, 0)
    keybow.set_pixel(4, 192, 64, 0)
    keybow.set_pixel(5, 192, 64, 0)
    keybow.set_pixel(6, 192, 64, 0)
    keybow.set_pixel(7, 192, 64, 0)
    keybow.set_pixel(8, 192, 64, 0)
    keybow.set_pixel(9, 128, 0, 0)
    keybow.set_pixel(10, 128, 128, 0)
    keybow.set_pixel(11, 0, 0, 128)
end

-- Standard number pad mapping --

-- Key mappings --

function handle_key_00(pressed)
    if pressed then
        keybow.set_modifier(keybow.LEFT_META, keybow.KEY_DOWN)
        keybow.tap_key("r", pressed)
        keybow.set_modifier(keybow.LEFT_META, keybow.KEY_UP)
    end
end

function handle_key_01(pressed)
    keybow.set_pixel(1, 255, 255, 0)
    keybow.set_key(".", pressed)
end

function handle_key_02(pressed)
    keybow.set_key(keybow.ENTER, pressed)
end

function handle_key_03(pressed)
    keybow.set_key("1", pressed)
end

function handle_key_04(pressed)
    keybow.set_key("2", pressed)
end

function handle_key_05(pressed)
    keybow.set_key("3", pressed)
end

function handle_key_06(pressed)
    keybow.set_key("4", pressed)
end

function handle_key_07(pressed)
    keybow.set_key("5", pressed)
end

function handle_key_08(pressed)
    keybow.set_key("6", pressed)
end

function handle_key_09(pressed)
    keybow.set_pixel(9, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py red")
    --    win_snippets.run("python \"D:\\denva\\src\\overseer\\manual_status_override.py\" red")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(9, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(9, 128, 0, 0)
end

function handle_key_10(pressed)
    keybow.set_pixel(10, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py yellow")
    --    win_snippets.run("python \"D:\\denva\\src\\overseer\\manual_status_override.py\" red")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(10, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(10, 128, 128, 0)
end

function handle_key_11(pressed)
    keybow.set_pixel(11, 0, 64, 192)
    win_snippets.run("cmd")
    keybow.sleep(100)
    keybow.text("python B:\\GitHub\\denva\\src\\overseer\\manual_status_override.py")
    --    win_snippets.run("python \"D:\\denva\\src\\overseer\\manual_status_override.py\" red")
    keybow.sleep(300)
    keybow.tap_enter()
    keybow.set_pixel(11, 64, 64, 64)
    keybow.text("exit")
    keybow.tap_enter()
    keybow.sleep(500)
    keybow.set_pixel(11, 0, 0, 128)
end
