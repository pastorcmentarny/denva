# List of useful commands

`cat /etc/os-release` - display version of os
`history > commands_history.txt` - save history of commands to file
`pgrep -af python` - display all python processes running

# Run it before turn it off Pi

```sudo halt```

# Update Pi

0. `sudo apt update`
0. `sudo apt full-upgrade`
0. `sudo apt clean`
0. `sudo apt autoremove`
0. `sudo reboot`
0. `sudo pip install --upgrade pip'`

## Pi related

* ``` i2cdetect -y 1``` display list i2c port used on
* ```sudo apt-get install postfix```

# check if process is running

ps -aux | grep "nc 192.168.0.201 30003" | grep -v grep ps -aux | grep "sudo
/home/pi/denva-master/scripts/dump_data_reader.sh" | grep -v grep

# if I lost pip

`python -m ensurepip`

# watch temp every second
watch -n 1 vcgencmd measure_temp
