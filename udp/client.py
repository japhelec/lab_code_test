#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
import threading


class UDPClient:
    def __init__(self):
        self.starttime = time.time()
        self.HOST = '0.0.0.0'
        self.PORT = 5566
        self.server_addr = (self.HOST, self.PORT)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.thread = threading.Thread(target=self._sendKey)
        self.thread.start()

        self.id_count = 5
        self.id_interval = 1


    def _sendKey(self):
        while True:
            print("==========")
            outdata = raw_input('please input message: ')

            if (outdata == "id"):
                mode = raw_input('please input id mode: ')

                count = 0
                while (1):
                    if (count <self.id_count):
                        self.s.sendto("rc 3 0 0 0".encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto("rc 0 0 0 0".encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto("rc -3 0 0 0".encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto("rc 0 0 0 0".encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        count += 1
                    else: 
                        break;
            else:
                print('sendto ' + str(self.server_addr) + ': ' + outdata)
                self.s.sendto(outdata.encode(), self.server_addr)

            if (outdata == "l"):
                break

client = UDPClient()