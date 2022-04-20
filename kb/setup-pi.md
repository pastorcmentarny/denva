# SETUP

## STATIC IP

In sudo nano /etc/dhcpcd.conf

* server 192.168.0.200/24
* denva 192.168.0.201/24
* denviro 192.168.0.202/24
* delight 192.168.0.203/24

```bash
interface wlan0
static ip_address=192.168.0.224/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

## Access Pi via Windows
1```sudo apt-get install samba```
2```sudo nano /etc/samba/smb.conf```
3 Add this:
   ```
   [trases]
   path = /home/ds
   guest ok = yes
   read only = no
   ```
4. make home directory writeable to all: ```sudo chmod a+w /home/pi/```

## Reduce write/read of SD card to prevent data corruption and life span of SD card

```bash
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile
sudo apt-get install busybox-syslogd
sudo apt-get remove --purge rsyslog

```

## Add ability to connect to Remote Desktop

`sudo apt-get install xrdp`

# ==== ==== ==== ==== ==== ==== ====

## Setup Welcome page after logon

`/etc/motd` to edit welcome page after login

## Set hostname

to set name of the device
```sudo nano /etc/hostname```
```sudo nano /etc/hosts```


# Setup mounts and drives

`/etc/fstab` to edit mounts to this Pi

## Add exfat support
`sudo apt-get install exfat-fuse`
`sudo apt-get install exfat-utils`

## Add ntfs support
to use ntfs partition
`sudo apt-get install ntfs-3g` 


## Setup ssd storage
1. `sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL` - check is ssd is there 
2. `mkdir storage` 
3. `sudo mount /dev/sdb1 /home/pi/storage -t exfat -o uid=pi,gid=pi`
4. `sudo chmod 777 /home/pi/storage/` 
5. `sudo nano /etc/fstab``
   1.add ``/dev/sda1             /home/pi/storage  exFAT defaults  0       0``
   

   
## Set device for mote lighting
sudo chmod 666 /dev/ttyACM0  

## SETUP CRONTAB
sudo crontab -e03 13 * * * /sbin/shutdown -r now


## Update Pi

0. `sudo apt update`
1. `sudo apt full-upgrade`
2. `sudo apt clean`
3. `sudo apt autoremove`
4. `sudo reboot`
5. `pip install --upgrade pip'`


## Update eeprom

sudo rpi-eeprom-update
sudo rpi-eeprom-update -a
sudo reboot


## Install java17 

sudo apt install zip
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk list java

(https://sdkman.io/install)
