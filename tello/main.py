import sdk as tello
from camera import Camera
from pose_estimation import pose_estimation

import cv2
from threading import Thread
from control import control
import time
import keyboard 


keepread = True
isControl = False
drone = tello.Tello('', 8889)  
camera = Camera()

# recv image
def recvImage():
    while keepread:
        frame = drone.read()
        if frame is None or frame.size == 0:
            continue 
        
        LP_pose = pose_estimation(frame, camera)

        global isControl
        if (isControl):
            control(drone, LP_pose)

    cv2.destroyAllWindows()

# keyborad
def recvkeybord(): 
    while True:
        key = keyboard.read_key()

        if key == "o": #takeoff
            drone.send_command("takeoff")
            time.sleep(2)
        elif key == "v": #vision
            camera.switch_vision()
            drone.send_command("downvision " + str(camera.vision.value))
            time.sleep(1)
        elif key == "i": #control switch
            global isControl
            isControl = not isControl
            time.sleep(1)
        

        elif key == "w": #move forward
            drone.send_command("rc 0 30 0 0")
            time.sleep(1)
        elif key == "a": #move left
            drone.send_command("rc -30 0 0 0")
            time.sleep(1)
        elif key == "s": #move backward
            drone.send_command("rc 0 -30 0 0")
            time.sleep(1)
        elif key == "d": #pause right
            drone.send_command("rc 30 0 0")
            time.sleep(1)
        elif key == "q": #move up
            drone.send_command("rc 0 0 30 0")
            time.sleep(1)
        elif key == "e": #move down
            drone.send_command("rc 0 0 -30 0")
            time.sleep(1)
        elif key == "p": #pause
            drone.send_command("stop")
            time.sleep(1)

        elif key == "l": #land
            drone.send_command("land")
            global keepread
            keepread = False
            break




tImage = Thread(target=recvImage)
tImage.start() 

tKeyboard = Thread(target=recvkeybord)
tKeyboard.start()

tImage.join()
print("Tello control end")