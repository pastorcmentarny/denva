#!/bin/bash

#this task is to update to newest version and reboot

branch = "master"

    echo "killing app and server"
    sudo kill $(ps aux | grep '[p]ython3' | awk '{print $2}' | xargs sudo kill -15 )
    echo "removing existing apps"
    cd /home/pi
    rm "$branch.zip"
    rm -rf "denva-$branch"
    echo "installing new version from github"
    wget "https://github.com/pastorcmentarny/denva/archive/$1.zip"
    unzip "$1.zip"
    echo "rebooting Pi"
    sudo reboot