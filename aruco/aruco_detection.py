import numpy as np
import time
import cv2
import cv2.aruco as aruco

frame=cv2.imread('./Resources/picture_1.jpg')

# frame=cv2.resize(frame,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_CUBIC)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

parameters =  aruco.DetectorParameters_create()

corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)

aruco.drawDetectedMarkers(frame, corners,ids)


cv2.imshow("frame",frame)
cv2.waitKey(5000)
cv2.destroyAllWindows()
