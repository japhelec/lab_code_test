import sdk as tello

import time, cv2
from threading import Thread
import keyboard 


keepread = True
drone = tello.Tello('', 8889)  

def streaming():
    while keepread:
        frame = drone.read()
        if frame is None or frame.size == 0:
            continue 
        cv2.imshow('img', frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()

vsm = Thread(target=streaming)
vsm.start()

# keyborad
def recvkeybord(): 
    while True:
        if keyboard.is_pressed('c'):
            global keepread
            keepread = False
            break
        if keyboard.is_pressed('d'):
            drone.send_command("downvision 1")
        if keyboard.is_pressed('f'):
            drone.send_command("downvision 0")
            

ss = Thread(target=recvkeybord)
ss.start()



vsm.join()
print("Tello control end")