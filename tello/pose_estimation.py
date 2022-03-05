import numpy as np
import cv2
from cv2 import aruco
from camera import CameraVision
from coordinateTransform import Rx, Ry, Rz

# ======================
# ArUco marker coordinate
# [Forward]
#
#         +z
#       ------
#       |    |
#       |  B |  +x
#       |    |
#       ------
#
# [Downward]
#
#       ------
#       |    |
#    +y |  B |  
#       |    |
#       ------
#         +x
#
# ======================


ARUCO_SIDE_LENGTH = 7.08 # in meters
DEBUG = False # whether show frame
font = cv2.FONT_HERSHEY_SIMPLEX

def CT_Aruco_to_Body(vision):
    if (vision == CameraVision.FORWARDVISION):
        return Rx(-90)
    elif (vision == CameraVision.DOWNVISION):
        return Rx(180).dot(Rz(90))




def pose_estimation(frame, camera):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    ## detect
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
    if ids is not None:
        
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIDE_LENGTH, camera.get_mtx(), camera.get_dist())
        
        CT = CT_Aruco_to_Body(camera.get_vision())
        
        if (DEBUG):
            (rvec-tvec).any()

            for i in range(rvec.shape[0]):
                aruco.drawAxis(frame, camera.get_mtx(), camera.get_dist(), rvec[i, :, :], tvec[i, :, :], 0.03)
                aruco.drawDetectedMarkers(frame, corners)
        
            cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            cv2.imshow("frame",frame)
            cv2.waitKey(1)

        return CT.dot(tvec[0].T)
        

    else:
        if (DEBUG):
            cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            cv2.imshow("frame",frame)
            cv2.waitKey(1)
        
        return None