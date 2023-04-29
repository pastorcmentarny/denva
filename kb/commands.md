# List of useful commands

* `cat /etc/os-release` - display version of os
* `pgrep -af python` - display all python processes running
* `vcgencmd get_camera` - to check if camera is supported and detected
* `lsusb` - to see list of usb devices connected to Pi
* `v4l2-ctl --list-formats-ext` - check what resolution are supported
* `sudo chmod -R MODE DIRECTORY` - set permission for directory
* `uname -m` - to check is it 64bit (arch64) or 32bit (armv7l) version of Raspberry Pi.
* `cat /var/spool/mail/pi` - to  email read messages when you see “You have new mail in /var/mail/pi”
* `> /var/spool/mail/pi` - delete messages in /var/mail/pi
* `dmesg` - Dmesg is the acronym for diagnostic message. Dmesg is a CLI utility in Linux that displays kernel-related messages retrieved from the kernel ring buffer.I use it to detect Out of Memory and Under Voltage issues 

# Run it before turn it off Pi

* ```sudo halt```

## Pi related

* ``` i2cdetect -y 1``` display list i2c port used on
* ```sudo apt-get install postfix```

# check if process is running

* `ps -aux | grep "nc 192.168.0.201 30003" | grep -v grep ps -aux | grep "sudo /home/pi/denva-master/scripts/dump_data_reader.sh" | grep -v grep`

# if I lost pip

* `python -m ensurepip`

# watch temp every second

* `watch -n 1 vcgencmd measure_temp`

# watch any file (for example measurement in trases4)

* `watch -n 1 cat /home/ds/data/measurement.txt`
