#!/bin/bash

DATA_DIR_DATE=$(date +'%Y/%m/%d')
DATA_PATH="/home/pi/data/${DATA_DIR_DATE}"
FILE_NAME="aircraft.txt"
echo "$DATA_PATH"
sudo mkdir -p "$DATA_PATH"
cd $DATA_PATH
sudo touch "$FILE_NAME"
# `tail -f /dev/null |`  allows me to run nc in background :)
tail -f /dev/null | nc  192.168.0.201 30003 >> "$DATA_PATH/$FILE_NAME" &
