#pylint:disable=no-member

import cv2 as cv

verify_picture_location = '/home/kuei/Documents/record/aruco/downward camera/795mm.jpg'

img = cv.imread(verify_picture_location)
cv.imshow('Cats', img)

cv.waitKey(0)

cv.destroyAllWindows()
