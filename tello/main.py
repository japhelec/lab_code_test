from termcolor import colored

import sdk as tello
from camera import Camera
from pose_estimation import pose_estimation

import cv2
from threading import Thread
from control import control
import keyboard 
import socket


keepread = True
isControl = False
drone = tello.Tello('', 8889)  
camera = Camera()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5566))

# recv image
def recvImage():
    while keepread:
        print("=========") # split line for distinguish each loop
        frame = drone.read()
        if frame is None or frame.size == 0:
            # print("no image")
            continue 
        
        LP_pose = pose_estimation(frame, camera)
        if LP_pose is None:
            # print("no aruco")
            continue 

        print("aruco pose: %d, %d, %d" % (LP_pose[0][0], LP_pose[1][0], LP_pose[2][0]))
        global isControl
        if (isControl):
            control(drone, LP_pose)

    cv2.destroyAllWindows()

# keyborad
def recvkeybord():
    print("server start listening for key events at PORT 5566...")         
    while True:
        indata, addr = s.recvfrom(1024) # blocking mode
        key = indata.decode()

        if key == "o": #takeoff
            print(colored("[command] takeoff!", "green"))
            drone.send_command("takeoff")
        elif key == "v": #vision
            print(colored("[command] vision!", "green"))
            camera.switch_vision()
            drone.send_command("downvision " + str(camera.vision.value))
        elif key == "i": #control switch
            print(colored("[command] control!", "green"))
            global isControl
            isControl = not isControl
        

        elif key == "w": #move forward
            print(colored("[command] move forward!", "green"))
            drone.send_command("rc 0 30 0 0")
        elif key == "a": #move left
            print(colored("[command] move left!", "green"))
            drone.send_command("rc -30 0 0 0")
        elif key == "s": #move backward
            print(colored("[command] move backward!", "green"))
            drone.send_command("rc 0 -30 0 0")
        elif key == "d": #pause right
            print(colored("[command] move right!", "green"))
            drone.send_command("rc 30 0 0")
        elif key == "q": #move up
            print(colored("[command] move up!", "green"))
            drone.send_command("rc 0 0 30 0")
        elif key == "e": #move down
            print(colored("[command] move down!", "green"))
            drone.send_command("rc 0 0 -30 0")
        elif key == "p": #pause
            print(colored("[command] stop!", "green"))
            drone.send_command("stop")

        elif key == "l": #land
            print(colored("[command] land!", "green"))
            drone.send_command("land")
            global keepread
            keepread = False
            s.close()
            break




# tImage = Thread(target=recvImage)
# tImage.start() 

tKeyboard = Thread(target=recvkeybord)
tKeyboard.start()

# tImage.join()
print("Tello control end")