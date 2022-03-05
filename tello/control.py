import numpy as np

CONTROL_SATURATION = 100

P = np.array([
    [1.5,0,0],
    [0,1.5,0],
    [0,0,1.5]
    ]) # shape (3,3)

I = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1]
    ]) # shape (3,3)

D = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1]
    ]) # shape (3,3)



def control(tello, lp):
    # lp of shape (3,1)
    # lp is coordinate of landing pad relative to drone camera,
    F = P.dot(lp)
    F = np.floor(F)

    np.clip(F, -CONTROL_SATURATION, CONTROL_SATURATION, out=F)
    
    tello.send_command("rc %d %d %d %d" % (F[0][0], F[1][0], F[2][0], 0))
    # print("rc %d %d %d %d" % (F[0][0], F[1][0], F[2][0], 0))
    