# import the necessary packages
import numpy as np
import argparse
import cv2

im = cv2.imread('/var/www/test/test.jpg')
cv2.imshow("im", im)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
cv2.imshow("Thresh", thresh)
(cnts, _) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#(cnts, _) = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im,cnts,-1,(0,255,0),3)
cv2.drawContours(im,cnts,-1,(0,255,0),-1)
cv2.imshow("Image",im)
cv2.waitKey(0)
