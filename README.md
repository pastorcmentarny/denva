# Denva - it starts as Dom's Environment Analyser and become denva is a Dom's personal assistant

This project has inspired by various events in the workplace. It measures:

- Shaking leg detector is a feature that was inspired by the fact that when I enjoy programming and listen to good
  music, I start shaking my legs, so this sensor will warn me with flashing LEDs when I do that, so my beloved colleague
  does not suffer from earthquake experience on their desk. It uses a motion sensor.
- Temperature (AC and heating systems have a love/hate relationship in the office, so I want to track when our office is
  the oven or freezer mode)
- Pressure (This does NOT measure pressure from managers at work, but it measures weather pressure. I do not need it but
  as one of the sensor returns this date, so I display it.
- Humidity (The humidity can affect productivity)
- Brightness and colour (to check how dark is in the office at night)
- The UV index ( I used this at home, so then I know do I need lots of UV cream or not.

I am planning to add:

- Indoor air quality
- dBm measurement

Design choices

- Mono-repo

This project is written in Python 3 and uses:

On Denva device:

- Raspberry Pi 4 (4GB)
- Pimoroni Breakout Garden HAT
- BH1745 Luminance and Colour Sensor Breakout
- BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor
- ICM20948 9DoF Motion Sensor Breakout
- VEML6075 UVA/B Sensor Breakout
-

On Denviro device:

- Raspberry Pi 3 Model B+
- Enviro+
- PMS 5003 to measure pollution

On Delight device:

- Raspberry Pi 3 Model (Kano)
- Unicorn HAT HD

Server:

- LattePanda Delta 432 with WD Blue SN500
- Logitech Logitech C525
- Anker USB 3.0 AK-A7507011

## DESIGN

- Denva App
    - _Get all sensor data_
    - _Send all data to server_
    - _Store all data locally_

- Enviro App
    - _Get all sensor data_
    - _Send all data to server_
    - _Store all data locally_

- Server App
    - _Send email with data every 5 minutes_
    - _Remove all images that are black_
- Server CAMERA APP _Python app that making photos_


- Server UI __
    - Move

carbon monoxide (reducing), nitrogen dioxide (oxidising), and ammonia (NH3),

resources:

0. https://www.idt.com/eu/en/document/whp/overview-tvoc-and-indoor-air-quality
0. https://www.epa.gov/sites/production/files/2014-05/documents/zell-aqi.pdf


https://www.google.com/appsstatus