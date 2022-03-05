import socket

class KeyServer:
    def __init__(self):
        self.HOST = '0.0.0.0'
        self.PORT = 5566
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((HOST, PORT))
        print('server start at: %s:%s' % (HOST, PORT))
        print('wait for connection...')

    def listen(self):
        while True:
        print("======")
        indata, addr = s.recvfrom(1024)
        print('recvfrom ' + str(addr) + ': ' + indata.decode())

        outdata = 'echo ' + indata.decode()
        s.sendto(outdata.encode(), addr)

        if (indata.decode() == "c"):
            print("here")
            s.close()
            break