import socket
import threading
from termcolor import colored


# wsl cannot detect keyboard
# choose to use socket to interact

class Keyboard:
    """Wrapper class to interact with the Tello drone."""

    def __init__(self, drone, act, view):
        self.drone = drone
        self.act = act
        self.view = view
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 5566))

        self.thread = threading.Thread(target=self._recvkeybord)
        self.thread.daemon = True

        self.thread.start()

    
    def __del__(self):
        self.socket.close()
        self.socket_video.close()

    def _recvkeybord(self):
        print("server start listening for key events at PORT 5566....\n")         
        while True:
            try:
                indata, addr = self.socket.recvfrom(1024) # blocking mode
                key = indata.decode()


                # =========================
                # drone related
                # =========================
                if key == "o": #takeoff
                    print(colored("[command] takeoff!", "green"))
                    self.drone.send_command("takeoff")        
                elif key == "w": #move forward
                    print(colored("[command] move forward!", "green"))
                    self.drone.send_command("rc 0 10 0 0")
                elif key == "a": #move left
                    print(colored("[command] move left!", "green"))
                    self.drone.send_command("rc -10 0 0 0")
                elif key == "s": #move backward
                    print(colored("[command] move backward!", "green"))
                    self.drone.send_command("rc 0 -10 0 0")
                elif key == "d": #pause right
                    print(colored("[command] move right!", "green"))
                    self.drone.send_command("rc 10 0 0")
                elif key == "q": #move up
                    print(colored("[command] move up!", "green"))
                    self.drone.send_command("rc 0 0 10 0")
                elif key == "e": #move down
                    print(colored("[command] move down!", "green"))
                    self.drone.send_command("rc 0 0 -10 0")
                elif key == "v": #vision
                    print(colored("[command] vision!", "green"))
                    self.drone.camera.switch_vision()
                    self.drone.send_command("downvision " + str(self.drone.camera.vision.value))
                

                # =========================
                # action related
                # =========================
                elif key == "c": #control start
                    print(colored("[command] control!", "green"))
                    self.act.set_control_mode(True)
                elif key == "p": # control stop
                    print(colored("[command] stop!", "green"))
                    self.act.set_control_mode(False)
                    self.drone.send_command("stop")
                
                elif key == "l": #land
                    print(colored("[command] land!", "green"))
                    self.act.set_control_mode(False)
                    self.drone.send_command("land")
                    break
       
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)