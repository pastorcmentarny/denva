## ' Cannot access to console, the root account is locked' after modify /etc/fstab
Solution:
1. Take SD card and insert to reader on PC
2. In cmdline.txt in boot partion add init=/bin/sh
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
11. It should works now :D