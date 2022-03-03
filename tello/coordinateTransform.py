import numpy as np

# *******************
# Two frames A, B
# A rotate "theta" along x axis of A, resulting in B
# P_A = Rx * P_B

# theta in degrees
# *******************
def Rx(degree):
    rad = np.radian(degree)

    return np.array([
        [1, 0, 0],
        [0, np.cos(rad), -np.sin(rad)], 
        [0, np.sin(rad), np.cos(rad)]
        ])

def Ry(degree):
    rad = np.radian(degree)

    return np.array([
        [np.cos(rad), 0, np.sin(rad)],
        [0, 1, 0], 
        [-np.sin(rad), 0, np.cos(rad)]
        ])

def Rz(degree):
    rad = np.radian(degree)

    return np.array([
        [np.cos(rad), -np.sin(rad), 0],
        [np.sin(rad), np.cos(rad), 0], 
        [0, 0, 1]
        ])