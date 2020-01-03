
`/etc/motd` to edit welcome page after login
`/etc/fstab` to edit mounts to this Pi


Install:
```bash
# disable swapfile as I don't need .It reducs amount write/read of SD card.It is not for perofrmance
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
```