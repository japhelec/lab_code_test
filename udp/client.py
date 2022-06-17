#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
import threading


common_command = {}
common_command["id"] = {}
common_command["id"]["h"] = "m 0 0 0 0"
common_command["id"]["x"] = {}
common_command["id"]["y"] = {}
common_command["id"]["z"] = {}
common_command["id"]["t"] = {}
common_command["id"]["x"]["p"] = "m 80 0 0 0"
common_command["id"]["x"]["n"] = "m -80 0 0 0"
common_command["id"]["y"]["p"] = "m 0 20 0 0"
common_command["id"]["y"]["n"] = "m 0 -20 0 0"
common_command["id"]["z"]["p"] = "m 0 0 20 0"
common_command["id"]["z"]["n"] = "m 0 0 -20 0"
common_command["id"]["t"]["p"] = "m 0 0 0 20"
common_command["id"]["t"]["n"] = "m 0 0 0 -20"

class UDPClient:
    def __init__(self):
        self.starttime = time.time()
        self.HOST = '0.0.0.0'
        self.PORT = 5566
        self.server_addr = (self.HOST, self.PORT)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.thread = threading.Thread(target=self._sendKey)
        self.thread.start()

        self.id_count = 1
        self.id_interval = 4


    def _sendKey(self):
        while True:
            print("==========")
            outdata = raw_input('please input message: ')

            if (outdata == "id"):
                mode = raw_input('please input id mode: ')

                self.s.sendto("c".encode(), self.server_addr)

                count = 0
                time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                
                while (1):
                    if (count <self.id_count):
                        count += 1
                        print("current count: %d" % (count)) 
                        self.s.sendto(common_command["id"][mode]["n"].encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto(common_command["id"]["h"].encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto(common_command["id"][mode]["p"].encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                        self.s.sendto(common_command["id"]["h"].encode(), self.server_addr)
                        time.sleep(self.id_interval - ((time.time() - self.starttime) % self.id_interval))
                    else: 
                        self.s.sendto("p".encode(), self.server_addr)
                        break;
            else:
                print('sendto ' + str(self.server_addr) + ': ' + outdata)
                self.s.sendto(outdata.encode(), self.server_addr)

            if (outdata == "l"):
                break

client = UDPClient()