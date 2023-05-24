# SETUP

## STATIC IP

In `sudo nano /etc/dhcpcd.conf`

* server 192.168.0.200/24
* denva 192.168.0.201/24
* denviro 192.168.0.202/24
* delight 192.168.0.203/24
* mobile 192.168.0.204/24
* denvaTwo 192.168.0.205/24
* I used 206
* ubercorn 192.168.0.208/24

```bash
interface wlan0
static ip_address=192.168.0.208/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

## Access Pi via Windows

1```sudo apt-get install samba```
2```sudo nano /etc/samba/smb.conf```
3 Add this:

   ```
   [device]
   path = /home/ds
   guest ok = yes
   read only = no
   ```

4. make home directory writeable to all: ```sudo chmod a+w /home/ds/```

## Reduce write/read of SD card to prevent data corruption and life span of SD card

```bash
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile && \ 
sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile && \
sudo apt-get install busybox-syslogd && \
sudo apt-get remove --purge rsyslog

```

## Add ability to connect to Remote Desktop

`sudo apt-get install xrdp`

## Setup Welcome page after logon

* `/etc/motd` to edit welcome page after login

## Set hostname

to set name of the device

```
sudo nano /etc/hostname
sudo nano /etc/hosts
```

# Setup mounts and drives

`/etc/fstab` to edit mounts to this Pi

## Add exfat support

```
sudo apt-get install exfat-fuse`
sudo apt-get install exfat-utils`
```

## Add ntfs support

* to use ntfs partition
  `sudo apt-get install ntfs-3g`

## Setup ssd storage

1. `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL` - check is ssd is there
2. `mkdir storage`
3. `sudo mount /dev/sdb1 /home/pi/storage -t exfat -o uid=pi,gid=pi`
4. `sudo chmod 777 /home/pi/storage/`
5. `sudo nano /etc/fstab``
   1.add ``/dev/sda1 /home/pi/storage exFAT defaults 0 0``

## Set device for mote lighting

* sudo chmod 666 /dev/ttyACM0

## SETUP CRONTAB

* sudo crontab -e03 13 * * * /sbin/shutdown -r now



## Install java17

```
sudo apt install zip
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk list java

(https://sdkman.io/install)
```


## Setup usb stick to reboot device on insert
1. Insert USB stick.
2. run the command 'lsusb' to find  ID of USB stick.
```bash
$ lsusb
Bus 001 Device 001: ID d00e:8686 Usb Stick
Bus 001 Device 002: ID 42e1:4554 Realtek Semiconductor Corp. RTL8188CUS 802.11n WLAN Adapter
```
3. ID is split into vendor(d00e) and product(8686)
4. `sudo nano /etc/udev/rules.d/10-poweroff.rules`
5. add  `ACTION=="add", ATTRS{idVendor}=="d00e", ATTRS{idProduct}=="8686", RUN+="/sbin/poweroff"`
6. Save it.
7. Remove the USB stick.
8. `sudo udevadm control --reload-rules`
9. Insert the USB stick. (Raspberry Pi)



Test: Progress Viewer - https://github.com/Xfennec/progress