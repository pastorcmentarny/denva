# Settings

## Setup Welcome page after logon

`/etc/motd` to edit welcome page after login

### Set hostname

to set name of the device
```sudo nano /etc/hostname```
```sudo nano /etc/hosts```


### Setup static ip

In sudo nano /etc/dhcpcd.conf

* server 192.168.0.200/24
* denva 192.168.0.201/24
* denviro 192.168.0.202/24
* delight 192.168.0.203/24

```bash
interface wlan0
static ip_address=192.168.0.203/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

### Setup mounts and drives

`/etc/fstab` to edit mounts to this Pi
`sudo apt-get install ntfs-3g` to use ntfs partition
`sudo apt-get autoremove`

## add ability to connect to Remote Desktop

`sudo apt-get install xrdp`

# Reduce rite/read of SD card to prevent data corruption and life span of SSD

```bash
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile
sudo apt-get install busybox-syslogd
sudo apt-get remove --purge rsyslog

```


## remove old alsa

sudo apt purge bluealsa sudo apt install pulseaudio-module-bluetooth rm ~/.asoundrc sudo apt purge pimixer


# set device for mote ligthing
sudo chmod 666 /dev/ttyACM0  


sudo crontab -e03 13 * * * /sbin/shutdown -r now

# Access to Pi via Windows 



1. ```sudo apt-get install samba```
2. ```sudo nano /etc/samba/smb.conf:```
3. Add this:
```[home]
path = /home/pi
guest ok = yes
read only = no
```
4. make home directory writeable to all: ```sudo chmod a+w /home/pi/```


Watchdog

It is useful to set up a watchdog which can reboot your RPi in case it renders unresponsive, we can use a watchdog kernel module for this purpose.

Load the watchdog kernel module:

$ sudo modprobe bcm2708_wdog

Add bcm2708_wdog into the /etc/modules so it gets loaded on boot.

$ sudo echo "bcm2708_wdog" >> /etc/modules

In addition to the kernel module, there is also a userspace daemon that we need:

$ sudo apt-get install watchdog

Examine the configuration file: /etc/watchdog.conf and configure it as appropriate for your situation.

Uncomment the line watchdog-device = /dev/watchdog

Uncomment the line with max-load-1

Setting a minimum free RAM amount is a good idea. Before starting the watchdog service, be prepared that you might have configured it incorrectly and it will reboot immediately when you start it and may continuously reboot after each boot. So be prepared to modify your SD card on a different device if that happens.

Enable  the watchdog to start at boot and start it now:

$ sudo insserv watchdog  
$ sudo /etc/init.d/watchdog start

During some modifications to your system (in read-write mode) later, you can consider disabling watchdog first. It rebooted my box once while I was doing some filesystem changes. Fortunately it booted fine for me, but it may not for you and may require manual, local fix.

In addition to the watchdog, you should set up reboot after a kernel panic. This is done by editing /etc/sysctl.conf. Add this line:

kernel.panic = 10

This will cause to wait 10 seconds after a kernel panic, then automatically safely reboot the box.

https://blog.ronnyvdb.net/2019/01/20/howto-make-a-raspberry-pi-truly-read-only-reliable-and-trouble-free/


https://sdkman.io/install