import sdk as tello
from camera import Camera
from pose_estimation import pose_estimation

import cv2
from threading import Thread
import time
import keyboard 


keepread = True
drone = tello.Tello('', 8889)  
camera = Camera()

# recv image
def recvImage():
    while keepread:
        frame = drone.read()
        if frame is None or frame.size == 0:
            continue 
        pose_estimation(frame, camera)

    cv2.destroyAllWindows()

# keyborad
def recvkeybord(): 
    while True:
        if keyboard.is_pressed('c'):
            global keepread
            keepread = False
            break
        if keyboard.is_pressed('s'):
            camera.switch_vision()
            drone.send_command("downvision " + str(camera.vision.value))
            time.sleep(2)




tImage = Thread(target=recvImage)
tImage.start() 

tKeyboard = Thread(target=recvkeybord)
tKeyboard.start()

tImage.join()
print("Tello control end")