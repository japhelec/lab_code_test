import cv2
import threading
from threading import _Timer

import numpy as np
import os
from termcolor import colored
from datetime import datetime


from control import Control
from perception import Perception

import time


class Action:
    def __init__(self, drone):
        self.drone = drone
        self.control = Control()
        self.perception = Perception(drone.camera)
        
        self.last_command = np.array([[0],[0],[0]])
        self.starttime = time.time()

        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H:%M:%S")

        self.f_if_pose = open(os.path.dirname(__file__) + "/../record/pose/pose_record_" + dt_string + ".csv", "a")
        self.f_if_pose.write("x,y,z\n")
        self.f_if_control = open(os.path.dirname(__file__) + "/../record/control/control_record_" + dt_string + ".csv", "a")
        self.f_if_control.write("roll,pitch,thrust,yaw\n")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(os.path.dirname(__file__) + "/../record/video/video_record_" + dt_string + ".avi", fourcc, 10.0, (320,240))


        self.toControl = False
        self.thread = threading.Thread(target=self._feedback_thread)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.f_if_pose.close()
        self.f_if_control.close()
        self.video.release()

    def _feedback_thread(self):
        while (1):
            time.sleep(0.1 - ((time.time() - self.starttime) % 0.1))
            print('============================================')
            print('1: ', datetime.now())
            frame = self.drone.read()
            print('2: ', datetime.now())
            if frame is None or frame.size == 0:  # add black frame
                if (self.drone.camera.get_vision().value == 0) :
                    frame = np.zeros((self.drone.camera.front_frame_size), dtype='uint8') # opencv and numpy dimension reverse
                else:
                    frame = np.zeros(self.drone.camera.down_frame_size, dtype='uint8')
            
            # get pose
            pose = self.perception.get_pose(frame)
            print('3: ', datetime.now())
            isPoseNone = False
            if pose is None:
                isPoseNone = True
                print("[pose]: NO")
            else: 
                print("[pose]: ", pose)

            # get control
            command = 0
            if (isPoseNone):
                print("[command]: NO")
            else:
                command = self.control.pid(pose)
                self.last_command = command
                print("[command]: ", command)
            print('4: ', datetime.now())

            
            # Save?
            # print("pose: ", pose)
            if (self.toControl):
                if (isPoseNone):
                    self.f_if_control.write("%d,%d,%d,%d\n" % (self.last_command[0][0], self.last_command[1][0], self.last_command[2][0], 0))
                    self.f_if_pose.write("N/A,N/A,N/A\n")
                    print('5: ', datetime.now())
                    # response = self.drone.send_command("rc %d %d %d %d" % (self.last_command[0][0], self.last_command[1][0], self.last_command[2][0], 0))
                    response = self.drone.send_command("rc %d %d %d %d" % (0, 0, 0, 0))
                    # print('response: ', response);
                    print('6: ', datetime.now())
                else:
                    self.f_if_control.write("%d,%d,%d,%d\n" % (command[0][0], command[1][0], command[2][0], 0))
                    self.f_if_pose.write("%f,%f,%f\n" % (pose[0][0], pose[1][0], pose[2][0]))
                    print('5: ', datetime.now())
                    # response = self.drone.send_command("rc %d %d %d %d" % (command[0][0], command[1][0], command[2][0], 0))
                    response = self.drone.send_command("rc %d %d %d %d" % (0, 0, 0, 0))
                    # print('response: ', response);
                    print('6: ', datetime.now())
                self.video.write(frame)
                print('7: ', datetime.now())

    
    def set_control_mode(self, mode):
        if (self.get_control_mode() and (not mode)):
            self.f_if_pose.close()
            self.f_if_control.close()
            self.video.release()

        self.toControl = mode

    def get_control_mode(self):
        return self.toControl