#####Edit file
`sudo nano .bashrc`

#####Aliases used on pi
* `alias denva-la ='tail -n 300 /home/pi/logs/logs.log'`
* `alias denva-ls ='tail -n 300 /home/pi/logs/server.log'`
* `alias denva-lh ='tail -n 300 /home/pi/logs/healthcheck.log'`
* `alias denva=update ='sudo bash /home/pi/denva-master/scripts/update.sh master app'`
