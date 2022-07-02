#####Edit file
`sudo nano .bashrc`

#####Aliases used on pi
* `alias denva-la ='tail -n 300 /home/pi/logs/logs.log'`
* `alias denva-ls ='tail -n 300 /home/pi/logs/server.log'`
* `alias denva-lh ='tail -n 300 /home/pi/logs/healthcheck.log'`
* `alias denva-update ='sudo bash /home/pi/denva-master/scripts/update.sh master app'`

## Aliases to run things on server:
```
alias kd='python3 /home/pi/knyszogar/knyszogar_display.py'
alias kw='python3 /home/pi/knyszogar/knyszogar_website.py'
alias ke='python3 /home/pi/knyszogar/knyszogar_email.py'
alias ka='python3 /home/pi/knyszogar/knyszogar_app.py'
alias kh='python3 /home/pi/knyszogar/knyszogar_net_hc.py'
alias tu='java -jar  /home/pi/transportmgr/ui/TransportManagerUI.jar'
alias ts='java -jar /home/pi/transportmgr/service/TransportManagerService.jar'
alias td='python3 /home/pi/transportmgr/db/db_app.py'
```
