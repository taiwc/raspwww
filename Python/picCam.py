# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:34:58 2017

@author: ASUS
"""
import numpy as np
import time
import sys
import io
import picamera
import cv2

with picamera.PiCamera() as camera:
    #camera.resolution=(640,480)
    camera.start_preview()
    print("Press Key to Save")
    #time.sleep(20)
    i=0
    while True:
        k=cv2.waitKey(500)
        if k==27: #ESC key to stop
            break
        else:
          filename="/var/www/image/image%02d.jpg" % i
          camera.capture(filename)
          print(filename)
          i=i+1
          if i>=20:
              break
          else:
              time.sleep(1)
    camera.stop_preview()
