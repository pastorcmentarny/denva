# Knyszogar - Personal Server Assistance

# source: https://ec.europa.eu/environment/air/quality/standards.htm

## DESIGN

Design choices

- Mono-repo
- Trunk Based Development
- Python 3


###

Project is split into main denva project that are run on sensor towers (under ```src``` folder ) and side projects (under ```projects``` that i need to mark as root source )

### Mothership (200)

It will contain various apps

- _Send email with data every 5 minutes_
- _Remove all images that are black_
- Server CAMERA APP _Python app that making photos_
- A server
- MessengerHub (Service responsible for sending email)
- CCTV
- Airplane scanner
- Sensor data processor
- Metrics Service - It will collect all metrics from all services

It runs all apps:

- app to
- healthcheck - to check application and connectivity
- email to send emails
- website - homepage + handling ui for all apps
- transport manager project
- Raspberry Pi 3 Model (Kano)

- It was LattePanda Delta 432 with WD Blue SN500
- Logitech Logitech C525
- Anker USB 3.0 AK-A7507011
-
- Mote (Controller + 4 APA102 RGB LED strips) - for status


- Server UI __
    - Move

carbon monoxide (reducing), nitrogen dioxide (oxidising), and ammonia (NH3),

### Denva(201) & Denva2(205) - it starts as Dom's Environment Analyser and become denva is a Dom's personal assistant

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

### Mothership (Server)

- Raspberry Pi 4 (8GB)
- Unicorn HAT HD

It used to run CCTV, lighting system, NAS but this was offload to Borg PC and LatePanda

### On Denva ONE device:

- Raspberry Pi 4 (4GB)
- Pimoroni Breakout Garden HAT
    1. MAX30101 Sensor - Heart Rate, Oximeter, Smoke Sensor
    2. BH1745 Luminance and Colour Sensor Breakout
    3. VEML6075 UVA/B Sensor Breakout
    4. SGP30 Air Quality Sensor
    5. SCD41 CO2 Sensor Breakout
    6. BME688 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor
    7. DVB-T+FM+DAB detect aircraft transceiver data

### On Denva TWO device:

- Raspberry Pi 4 (4GB)
- Pimoroni Breakout Garden HAT
    1. AS7262 Spectrometer
    2. PA1010D GPS sensor
    3. ICM20948 9DoF Motion Sensor
    4. MICS6814 3-in-1 Gas Sensor
    5. FREE SLOT
    6. ICP10125 air pressure sensor
    7. Mic to detect sound

##

app - where app is
logs - where logs is
data - where data
reports - where reports

## STATUS UI:

```
   1...5..........EF
  1 AA BB CC DD 
  2 
  3 aw cen 
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
  2 - DENVA2
  D - device status
  A - application
  U - ui for app
  AA - CPU TEMP
  BB - RAM
  CC - SPACE
  DD - NETWORK
  CCA - Camera A
  RRA - Radar App
  a - knyszogar app
  w - knyszogar website
  c - knyszogar config
  e - knyszogar email
  n = knyszogar network health check
  
```

# Resources:

0. https://www.idt.com/eu/en/document/whp/overview-tvoc-and-indoor-air-quality
1. https://www.epa.gov/sites/production/files/2014-05/documents/zell-aqi.pdf
2. https://www.google.com/appsstatus
