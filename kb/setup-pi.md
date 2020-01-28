
`/etc/motd` to edit welcome page after login
`/etc/fstab` to edit mounts to this Pi


Install:
```bash
# disable swap file as I don't need .It reduces amount write/read of SD card.It is not for performance
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile

# Below command fix this problem: Jan  6 23:19:05 raspberrypi CRON[431]: (CRON) info (No MTA installed, discarding  output)
sudo apt-get install postfix


sudo apt-get install ntfs-3g 
sudo apt-get autoremove

## Pi related
* ``` i2cdetect -y 1``` display list i2c port used on


```