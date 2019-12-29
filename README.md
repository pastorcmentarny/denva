# Denva - Dom's Environment Analyser

This project has inspired by various events in the workplace.
It measures:
- Shaking leg detector is a feature that was inspired by the fact that when I enjoy programming and listen to good music, I start shaking my legs, so this sensor will warn me with flashing LEDs when I do that, so my beloved colleague does not suffer from earthquake experience on their desk. It uses a motion sensor.
- Temperature (AC and heating systems have a love/hate relationship in the office, so I want to track when our office is the oven or freezer mode)
- Pressure (This do NOT measure pressure from managers at work, but it measures weather pressure. I do not need it but as one of the sensor returns this date, so I display it.
- Humidity (The humidity can affect productivity) 
- Brightness and colour (to check how dark is in the office at night)
- The UV index ( I used this at home, so then I know do I need lots of UV cream or not.

I am planning to add:
- Indoor air quality
- dBm measurement


This project is written in Python 3 and uses:
- Raspberry Pi 3 Model B+ 
- Pimoroni Breakout Garden HAT
- BH1745 Luminance and Colour Sensor Breakout
- BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor
- 1.12" Mono OLED (128x128, white/black) Breakout
- ICM20948 9DoF Motion Sensor Breakout
- VEML6075 UVA/B Sensor Breakout


## DESIGN

- Denva App 
    - _Get all sensor data_
    - _Send all data to server_
    - _Store all data locally_

- Denviroplas App 
    - _Get all sensor data_
    - _Send all data to server_
    - _Store all data locally_

- Server App
    - _Send email with data every 5 minutes_
    - _Remove all images that are black_
- Server CAMERA APP _Python app that making photos_


- Server UI __
    - Move 

