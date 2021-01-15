hack for keybow firmware

```lua
function keybow.set_key(key, pressed)
    if type(key) == "string" then
        local hid_code = nil
        local shifted = true
        if key == "\\" then
            hid_code = 0x64
            shifted = false
        elseif key == "|" then
            hid_code = 0x64
            shifted = true
        elseif key == "#" then
            hid_code = 0x32
            shifted = false
        elseif key == "~" then
            hid_code = 0x32
            shifted = true
        else
            hid_code = SHIFTED_KEYCODES:find(key, 1, true)
            if hid_code == nil then
                hid_code = KEYCODES:find(key, 1, true)
                shifted = false
            end
            hid_code = hid_code + 3
        end

        if not (hid_code == nil) then
            if shifted and pressed then keybow.set_modifier(keybow.LEFT_SHIFT, true) end
            keybow_set_key(hid_code, pressed)
            if shifted and not pressed then keybow.set_modifier(keybow.LEFT_SHIFT, false) end
        end

    else -- already a key code
        keybow_set_key(key, pressed)
    end
end
```