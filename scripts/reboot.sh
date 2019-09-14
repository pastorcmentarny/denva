#!/bin/bash

#taks: reboot with using newest version from master branch.
# it will be executed by cron job everyday
branch = "master"

#find all python process and kill it
sudo kill $(ps aux | grep '[p]ython3' | awk '{print $2}' | xargs sudo kill -15 )
cd /home/pi
#TODO add option if internet not available do not remove and try download
rm "$branch.zip"
rm -rf "denva-$branch"
wget "https://github.com/pastorcmentarny/denva/archive/$branch.zip"
unzip "$branch.zip"
cd "denva-$branch/"
cd "src/"
sudo python3 app.py
sudo python3 app_ui.py