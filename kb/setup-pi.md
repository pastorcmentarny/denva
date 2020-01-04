
`/etc/motd` to edit welcome page after login
`/etc/fstab` to edit mounts to this Pi


Install:
```bash
# disable swap file as I don't need .It reduces amount write/read of SD card.It is not for performance
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
```