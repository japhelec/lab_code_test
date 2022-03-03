import numpy as np
import cv2
from cv2 import aruco
from camera import Camera


ARUCO_SIDE_LENGTH = 0.0708 # in meters
font = cv2.FONT_HERSHEY_SIMPLEX


def pose_estimation(frame, camera):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    ## detect
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

    if ids is not None:

        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, ARUCO_SIDE_LENGTH, camera.get_mtx(), camera.get_dist())
    
        print("tvec", tvec)

        (rvec-tvec).any()

        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, camera.get_mtx(), camera.get_dist(), rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
    
        cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
    else:
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    cv2.imshow("frame",frame)
    cv2.waitKey(1)