#!/bin/bash

if [[ -z "$1" ]]
then
      echo "\$var is empty"
else
    echo "re-run project using branch $1"
    cd /home/pi
    rm "$1.zip"
    rm -rf "denva-$1"
    wget "https://github.com/pastorcmentarny/denva/archive/$1.zip"
    unzip "$1.zip"
    cd "denva-$1/"
    pip install -r "requirements.txt "
    cd "src/"
    sudo python3 app.py
fi
