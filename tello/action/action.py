import cv2
import threading
import numpy as np
import os
from termcolor import colored
from datetime import datetime


from control import Control
from perception import Perception


class Action:
    def __init__(self, drone):
        self.drone = drone
        self.control = Control()
        self.perception = Perception(drone.camera)
        
        self.last_command = np.array([[0],[0],[0]])

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
        while True:
            # get frame
            frame = self.drone.read()
            if frame is None or frame.size == 0:  # add black frame
                if (self.drone.camera.get_vision().value == 0) :
                    frame = np.zeros((self.drone.camera.front_frame_size), dtype='uint8') # opencv and numpy dimension reverse
                else:
                    frame = np.zeros(self.drone.camera.down_frame_size, dtype='uint8')
            
            # get pose
            pose = self.perception.get_pose(frame)
            isPoseNone = False
            if pose is None:
                isPoseNone = True
                # pose = np.array([[-999],[-999],[-999]])
                print("[pose]: NO")
            else: 
                print("[pose]: ", pose)

            # get control
            command = 0
            if (isPoseNone):
                # command = np.array([[-999],[-999],[-999]])
                print("[command]: NO")
            else:
                command = self.control.pid(pose)
                self.last_command = command
                print("[command]: ", command)

            
            # Save?
            # print("pose: ", pose)
            if (self.toControl):
                if (isPoseNone):
                    self.f_if_control.write("%d,%d,%d,%d\n" % (self.last_command[0][0], self.last_command[1][0], self.last_command[2][0], 0))
                    self.f_if_pose.write("N/A,N/A,N/A\n")
                    self.drone.send_command("rc %d %d %d %d" % (self.last_command[0][0], self.last_command[1][0], self.last_command[2][0], 0))
                else:
                    self.f_if_control.write("%d,%d,%d,%d\n" % (command[0][0], command[1][0], command[2][0], 0))
                    self.f_if_pose.write("%f,%f,%f\n" % (pose[0][0], pose[1][0], pose[2][0]))
                    self.drone.send_command("rc %d %d %d %d" % (command[0][0], command[1][0], command[2][0], 0))
                self.video.write(frame)

    
    def set_control_mode(self, mode):
        if (self.get_control_mode() and (not mode)):
            self.f_if_pose.close()
            self.f_if_control.close()
            self.video.release()

        self.toControl = mode

    def get_control_mode(self):
        return self.toControl