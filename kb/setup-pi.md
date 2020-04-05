
`/etc/motd` to edit welcome page after login
`/etc/fstab` to edit mounts to this Pi

### Set hostname
```sudo nano /etc/hostname```
```sudo nano /etc/hosts```
for name

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


# Below command fix this problem: Jan  6 23:19:05 raspberrypi CRON[431]: (CRON) info (No MTA installed, discarding  output)
sudo apt-get install postfix


sudo apt-get install ntfs-3g 
sudo apt-get autoremove

## Pi related
* ``` i2cdetect -y 1``` display list i2c port used on
