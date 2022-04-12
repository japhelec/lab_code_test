import numpy as np
from enum import Enum

class CameraVision(Enum):
    DOWNVISION = 1
    FORWARDVISION = 0

class Camera():
    def __init__(self):
        # forward camera
        self.fc_dist = np.array(([[0.02622212, -0.55220608, -0.0034407, 0.00321558, 1.89103285]]))

        self.fc_mtx = np.array([[901.57301941  , 0.      ,   477.52938592],
            [  0.       ,  907.36572961, 355.00994502],
            [  0.,           0.,           1.        ]])

        # downward camera
        self.dc_dist = np.array(([[0.172117726, -0.930775678, -0.000186194629, 0.000267682273, 2.64118271]]))

        self.dc_mtx = np.array([[349.09663679  , 0.      ,   164.50753375],
            [  0.       ,  349.26739721, 117.63836438],
            [  0.,           0.,           1.        ]])

        self.vision = CameraVision.FORWARDVISION

    def switch_vision(self):
        if self.vision == CameraVision.FORWARDVISION:
            self.vision = CameraVision.DOWNVISION
        elif self.vision == CameraVision.DOWNVISION:
            self.vision = CameraVision.FORWARDVISION

    def get_vision(self):
        return self.vision

    def get_mtx(self):
        if self.vision == CameraVision.FORWARDVISION:
            return self.fc_mtx
        elif self.vision == CameraVision.DOWNVISION:
            return self.dc_mtx

    def get_dist(self):
        if self.vision == CameraVision.FORWARDVISION:
            return self.fc_dist
        elif self.vision == CameraVision.DOWNVISION:
            return self.dc_dist