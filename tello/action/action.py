import threading
from termcolor import colored

from control import Control
from perception import Perception

class Action:
    def __init__(self, drone):
        self.drone = drone
        self.control = Control()
        self.perception = Perception(drone.camera)

        self.toControl = False
        self.thread = threading.Thread(target=self._feedback_thread)
        self.thread.daemon = True
        self.thread.start()

    def _feedback_thread(self):
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:
                continue 
            
            pose = self.perception.get_pose(frame)
            if pose is None:
                continue 
            
            print("pose: ", pose)
            if (self.toControl):
                command = self.control.pid(pose)
                self.drone.send_command(command)

    
    def set_control_mode(self, mode):
        self.toControl = mode

    def get_control_mode(self):
        return self.toControl