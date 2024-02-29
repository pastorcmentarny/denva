## ' Cannot access to console, the root account is locked' after modify /etc/fstab

Solution:

1. Take SD card and insert to reader on PC
2. In cmdline.txt in boot partition add init=/bin/sh
    1. `console=serial0,115200 console=tty1 root=PARTUUID=1add88fb-02 rootfstype=ext4 fsck.mode=force fsck.repair=yes rootwait init=/bin/sh`
    2. Save it
3. Insert SD card into Raspberry Pi
4. When bash is loaded
5. Type: `mount -o remount,rw /dev/mmcblk0p2 / `
6. Edit fstab `sudo nano /etc/fstab`
    1. Remove all stuff that cause problem
7. Turn off Pi
8. Take SD card and insert to reader on PC
9. Remove `init=/bin/sh` from cmdline.txt
10. Insert SD card into Raspberry Pi
11. It should work now :D

## Raspberry Pi do not start due to issue with sd card

Run on other linux device:
`sudo fsck -p /dev/sda1` - where sda1 is your location (you can check ) 


## due to database error unable to open database file File "/home/pi/knyszogar/db/db_service.py", line 19, in update_for  sqlite3.OperationalError: unable to open database file

pi@PISERVER:~ $ sudo chmod 776 knyszogar
pi@PISERVER:~ $ sudo chmod 776 -R knyszogar
pi@PISERVER:~ $ sudo chown pi:pi -R knyszogar
