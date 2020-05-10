#!/bin/bash

if [[ -z "$1" ]]
then
      echo "No params provided. You need 2 params branch and app to run. For example: sudo bash master app"
elif [[ -z "$2" ]]
then
      echo "only 1 param provided. You need 2 params branch and app to run. For example: sudo bash master app"
else
    echo "re-run project using branch $1"
    cd /home/pi
    echo "Backing up project file"
    mv "$1.zip" "$1-backup.zip"
    rm -rf "denva-$1"
    echo "Downloading new version of the project"
    wget "https://github.com/pastorcmentarny/denva/archive/$1.zip"
    echo "Installing new version"
    unzip "$1.zip"
    rm "$1-backup.zip"
    sudo chmod +x /home/pi/denva-master/scripts/dump_data_reader.sh
    echo "Running application"
    cd "denva-$1/"
    #pip install -r "requirements.txt "
    cd "src/"
    sudo python3 "$2.py"
fi
