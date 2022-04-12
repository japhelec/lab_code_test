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

        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H:%M:%S")

        self.f_if_pose = open(os.path.dirname(__file__) + "/../record/pose/pose_record_" + dt_string + ".csv", "a")
        self.f_if_pose.write("x,y,z\n")
        self.f_if_control = open(os.path.dirname(__file__) + "/../record/control/control_record_" + dt_string + ".csv", "a")
        self.f_if_control.write("roll,pitch,thrust,yaw\n")


        self.toControl = False
        self.thread = threading.Thread(target=self._feedback_thread)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.f_if_pose.close()

    def _feedback_thread(self):
        while True:
            # get frame
            frame = self.drone.read()
            if frame is None or frame.size == 0:  # add black frame
                if (self.drone.camera.get_vision().value == 0) :
                    frame = np.zeros(self.drone.camera.front_frame_size, dtype='uint8')
                else:
                    frame = np.zeros(self.drone.camera.down_frame_size, dtype='uint8')
            
            # get pose
            pose = self.perception.get_pose(frame)
            isPoseNone = False
            if pose is None:
                isPoseNone = True
                pose = np.array([[-999],[-999],[-999]])

            # get control
            command = 0
            if (isPoseNone):
                command = np.array([[-999],[-999],[-999]])
            else:
                command = self.control.pid(pose)
            
            # Save?
            print("pose: ", pose)
            if (self.toControl):
                self.f_if_control.write("%d,%d,%d,%d\n" % (command[0][0], command[1][0], command[2][0], 0))
                self.f_if_pose.write("%f,%f,%f\n" % (pose[0][0], pose[1][0], pose[2][0]))
                # self.drone.send_command("rc %d %d %d %d" % (command[0][0], command[1][0], command[2][0], 0))

    
    def set_control_mode(self, mode):
        self.toControl = mode

    def get_control_mode(self):
        return self.toControl