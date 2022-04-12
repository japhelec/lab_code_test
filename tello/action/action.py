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

        self.f_if_pose = open(os.path.dirname(__file__) + "/../record/pose_record_" + dt_string + ".csv", "a")
        self.f_if_pose.write("x,y,z\n")


        self.toControl = False
        self.toSave = False
        self.thread = threading.Thread(target=self._feedback_thread)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.f_if_pose.close()

    def _feedback_thread(self):
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:  # add black frame
                if (self.drone.camera.get_vision().value == 0) :
                    frame = np.zeros(self.drone.camera.front_frame_size, dtype='uint8')
                else:
                    frame = np.zeros(self.drone.camera.down_frame_size, dtype='uint8')
            
            pose = self.perception.get_pose(frame)
            if pose is None:
                pose = np.array([[-999],[-999],[-999]])
            
            print("pose: ", pose)
            # if (self.toControl):
            #     command = self.control.pid(pose)
            #     self.drone.send_command(command)
            
            if (self.toSave):
                self.f_if_pose.write("%f,%f,%f\n" % (pose[0][0], pose[1][0], pose[2][0]))

    
    def set_control_mode(self, mode):
        self.toControl = mode
        self.toSave = mode

    def get_control_mode(self):
        return self.toControl