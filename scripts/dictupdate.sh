#!/bin/bash

    FILE=/home/ds/denva-master/data/dictionary.txt

    cd /home/ds/denva-master/data/

    if test -f "$FILE"; then
        sudo mv dictionary.txt backup.txt
    fi

    wget "https://github.com/pastorcmentarny/DomLearnsChinese/raw/master/res/raw/dictionary.txt"

    if test -f "$FILE"; then
        echo "$FILE exist"
        sudo rm -f backup.txt
    fi
