#!/bin/bash

branch $1
echo "re-run project using branch " + branch
cd /home/pi
rm branch + ".zip"
rm -rf "denva-" + branch
wget "https://github.com/pastorcmentarny/denva/archive/" + branch + ".zip"
cd "denva-" + branch + "/src/"
sudo python3 app.py