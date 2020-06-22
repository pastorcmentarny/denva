### Setup Welcome page after logon
`/etc/motd` to edit welcome page after login


### Set hostname
to set name of the device
```sudo nano /etc/hostname```
```sudo nano /etc/hosts```

### Disable swap file as I don't need .
It reduces amount write/read of SD card.It is not for performance

```bash
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
```

### Setup static ip
In  sudo nano /etc/dhcpcd.conf

* server    192.168.0.200/24
* denva     192.168.0.201/24
* denviro   192.168.0.202/24
* delight   192.168.0.203/24

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
