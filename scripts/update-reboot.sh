#!/bin/bash

#this task is to update to newest version and reboot

branch = "master"

echo "killing app and server"
sudo kill $(ps aux | grep '[p]ython3' | awk '{print $2}' | xargs sudo kill -15 )
echo "Backing up project file"
mv "master.zip" "master-backup.zip"
rm -rf "denva-master"
echo "Downloading new version of the project"
wget "https://github.com/pastorcmentarny/denva/archive/master.zip"
echo "Installing new version"
unzip "master.zip"
rm "master-backup.zip"
sudo chmod +x /home/pi/denva-master/scripts/dump_data_reader.sh
pip3 install -r "requirements.txt "
echo "rebooting Pi"
sudo reboot