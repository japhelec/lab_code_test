import time, cv2
from threading import Thread
# from threading import Timer
from djitellopy import Tello
import keyboard 


# connect to Tello
tello = Tello()
tello.connect()

# video stream
keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoStreamer():
    while keepRecording:
        cv2.imshow('img', frame_read.frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

vsm = Thread(target=videoStreamer)
vsm.start()


# timer to stop stream
def stopStreaming(): 
    global keepRecording
    while True:
        if keyboard.is_pressed('c'):
            keepRecording = False
            break;
# timer = Timer(100.0, stopStreaming) 
ss = Thread(target=stopStreaming)
ss.start()



vsm.join()
tello.streamoff()
print("Tello control end")