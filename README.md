# Knyszogar - Personal Server Assistance

## DESIGN

Design choices
- Mono-repo
- Trunk Based Development
- Python 3

### Mothership (200)
Merge Delight into
It will contain various
- _Send email with data every 5 minutes_
- _Remove all images that are black_
- Server CAMERA APP _Python app that making photos_
- A server
- MessengerHub (Service responsible for sending email)
- CCTV
- Airplane scanner
- Sensor data processor
- Metrics Service - It will collect all metrics from all services


### Denva(201) & Denviro(202) - it starts as Dom's Environment Analyser and become denva is a Dom's personal assistant

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
- Pollution & Indoor air quality

## Hardware in use:

### Mothership

### On Denva device:

- Raspberry Pi 4 (4GB)
- Pimoroni Breakout Garden HAT
- BH1745 Luminance and Colour Sensor Breakout
- BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor
- ICM20948 9DoF Motion Sensor Breakout
- VEML6075 UVA/B Sensor Breakout


## On Denviro device:

- Raspberry Pi 3 Model B+
- Enviro+
- PMS 5003 to measure pollution


## On Delight device:

- Raspberry Pi 3 Model (Kano)
- Unicorn HAT HD


## Server:

- It was LattePanda Delta 432 with WD Blue SN500
- Logitech Logitech C525
- Anker USB 3.0 AK-A7507011
- 
- Mote (Controller  + 4 APA102 RGB LED strips) - for status



- Server UI __
    - Move

carbon monoxide (reducing), nitrogen dioxide (oxidising), and ammonia (NH3),



## STATUS UI:
   1...5..........EF
  1 AA BB CC DD 
  2 
  3 ka ke kn kw
  4 
  5 TU TS TD
  6 
  7 
  8
  9
  0     
  A             CCA           
  B 2D 2A 2U    
  C             RRA
  D 1D 1A 1U    
  E             RRD
  F     
  
  
  1 - DENVA
  2 - ENVIRO
  AA - CPU TEMP
  BB - RAM
  CC - SPACE
  DD - NETWORK
  CCA - Camera A
  RRA - Radar App
  ka - knyszogar app
  ke - knyszogar email
  kn = knyszogar network health check
  kw - knyszogar website


# Resources:
0. https://www.idt.com/eu/en/document/whp/overview-tvoc-and-indoor-air-quality
1. https://www.epa.gov/sites/production/files/2014-05/documents/zell-aqi.pdf
2. https://www.google.com/appsstatus
