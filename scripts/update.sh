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
    rm "$1.zip"
    rm -rf "denva-$1"
    wget "https://github.com/pastorcmentarny/denva/archive/$1.zip"
    unzip "$1.zip"
    cd "denva-$1/"
    #pip install -r "requirements.txt "
    cd "src/"
    sudo python3 "$2.py"
fi
