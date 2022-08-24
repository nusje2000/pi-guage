#!/usr/bin/env bash

DISPLAY=display@192.168.8.121
SERVER=pi@192.168.8.161

if [[ "$ALL" == 1 ]]; then
  ssh $DISPLAY "rm -rf ~/code; mkdir ~/code"
  ssh $SERVER "rm -rf ~/code; mkdir ~/code"

  scp -r ./display/* $DISPLAY:~/code
  scp -r ./server/* $SERVER:~/code
else
  scp -r ./display/main.py $DISPLAY:~/code
  scp -r ./server/src $SERVER:~/code
  scp -r ./server/package.json $SERVER:~/code
fi

ssh $SERVER "sudo systemctl restart data_collector.service" && echo "Restarted data collector"
ssh $DISPLAY "sudo systemctl restart data_display.service" && echo "Restarted data display"
