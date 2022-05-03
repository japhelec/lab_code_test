import numpy as np

class Control:
    def __init__(self):
        self.CONTROL_SATURATION_MAX = 25
        self.CONTROL_SATURATION_MIN= 8
        self.P = np.array([[2.0,0,0],[0,2.0,0],[0,0,0]]) # shape (3,3)
        self.I = np.array([[1,0,0],[0,1,0],[0,0,1]]) # shape (3,3)
        self.D = np.array([[1,0,0],[0,1,0],[0,0,1]]) # shape (3,3)

    def pid(self, lp):
        # lp of shape (3,1)
        # lp is coordinate of landing pad relative to drone camera,
        F = self.P.dot(lp)
        F = np.rint(F)

        ng = np.sign(F)

        np.absolute(F, out=F)
        np.clip(F, self.CONTROL_SATURATION_MIN, self.CONTROL_SATURATION_MAX, F)
        F = F*ng

        # np.clip(F, -self.CONTROL_SATURATION, self.CONTROL_SATURATION, out=F)

        return F
    