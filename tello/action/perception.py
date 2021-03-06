import numpy as np
import cv2
from cv2 import aruco
from coordinate import Rx, Ry, Rz, Tr

# ======================
# Camera Coordinate
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
# Body Coordinate
# [Forward]
#
#         +y
#       ------
#       |    |
#       |  B |  +x
#       |    |
#       ------
#
# ======================

class Perception:
    def __init__(self, camera, telloState):
        self.camera = camera
        self.telloState = telloState
        self.ARUCO_SIDE_LENGTH = 17.5 # in cm
        # self.DEBUG = False # whether show frame
        # font = cv2.FONT_HERSHEY_SIMPLEX

    def _RT_Camera_to_Body(self):
        if (self.camera.get_vision().value  == 0): # Forward vision
            return Rx(-90)
        elif (self.camera.get_vision().value == 1): # Downward vision
            return Rx(180).dot(Rz(90))

    def _RT_Camera_to_Body(self):
        if (self.camera.get_vision().value  == 0): # Forward vision
            return Rx(-90)
        elif (self.camera.get_vision().value == 1): # Downward vision
            return Rx(180).dot(Rz(90))

    def _LT_Camera_to_Body(self):
        if (self.camera.get_vision().value  == 0): # Forward vision
            return Tr(0, 3.2, 0) #3.2
        elif (self.camera.get_vision().value == 1): # Downward vision
            return Tr(0, -1.5, 0) #1.5

    def _CT_Body_to_Erect(self):
        return Rx(self.telloState.pitch).dot(Ry(self.telloState.roll))

    def get_pose(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()

        ## detect
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

        if ids is not None:    
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, self.ARUCO_SIDE_LENGTH, self.camera.get_mtx(), self.camera.get_dist())
            rt_C2B = self._RT_Camera_to_Body() # rotation transform from camera to body
            lt_C2B = self._LT_Camera_to_Body() # translation transform from camera to body
            ct_B2E = self._CT_Body_to_Erect() # coordinate transform from body to 
            # print('********************************************')
            # print("aruco: ", tvec)
            
            # ============= post processing ================
            # if (DEBUG):
            #     (rvec-tvec).any()

            #     for i in range(rvec.shape[0]):
            #         aruco.drawAxis(frame, cam.get_mtx(), cam.get_dist(), rvec[i, :, :], tvec[i, :, :], 0.03)
            #         aruco.drawDetectedMarkers(frame, corners)
            
            #     cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            #     cv2.imshow("frame",frame)
            #     cv2.waitKey(1)

            return ct_B2E.dot(lt_C2B + rt_C2B.dot(tvec[0].T))
            

        else:
            # ============= post processing ================
            # if (DEBUG):
            #     cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            #     cv2.imshow("frame",frame)
            #     cv2.waitKey(1)
            
            return None