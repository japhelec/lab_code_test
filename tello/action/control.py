import numpy as np

class Control:
    def __init__(self):
        self.CONTROL_SATURATION = 100
        self.P = np.array([[0.6,0,0],[0,0.6,0],[0,0,0.4]]) # shape (3,3)
        self.I = np.array([[1,0,0],[0,1,0],[0,0,1]]) # shape (3,3)
        self.D = np.array([[1,0,0],[0,1,0],[0,0,1]]) # shape (3,3)

    def pid(self, lp):
        # lp of shape (3,1)
        # lp is coordinate of landing pad relative to drone camera,
        F = self.P.dot(lp)
        F = np.floor(F)

        np.clip(F, -self.CONTROL_SATURATION, self.CONTROL_SATURATION, out=F)

        return ("rc %d %d %d %d" % (F[0][0], F[1][0], F[2][0], 0))
    