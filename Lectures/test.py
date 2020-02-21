import numpy as np
import imutils
import cv2

print("all packages imported")
img = cv2.imread("testudo.jpg")
cv2.imshow("image", img)
img_r = imutils.resize(img, width=400)
cv2.imshow("img",img_r)
cv2.imwrite("test.jpg",img_r)
cv2.waitKey(0)
