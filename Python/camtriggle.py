# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:34:58 2017

@author: ASUS
"""
import numpy as np
import time
import sys, getopt
import io
#import picamera
import picam as cam
import cv2

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    print(directory)
    try:
      os.stat(directory)
    except:
      os.mkdir(directory)
    #if not os.path.exists(directory):
    #    os.mkdir(directory)
    print(directory,"Ok")

def ShowImgWin(filen):
    im=cv2.imread(filen)
    cv2.imshow(filen,im)
    cv2.waitKey(0)

def ShowImgsWin(dirname,name,ext,loopi):
    for i in range(loopi):
        filen=dirname+"/"+name+"%02d"%i+ext
        ShowImgWin(filen)
    
def ShowImg(filen):
      showcmd="file_viewerNoCode.php?file="+filen+"";
      strmsg="<img src=\""+showcmd+"\""+" alt='"+filen+"' />"
      print(strmsg);

def ShowImgs(dirname,name,ext,loopi):
    for i in range(loopi):
        filen=dirname+"/"+name+"%02d"%i+ext
        ShowImg(filen)
      
def Triggle(dirname,name,ext,w,h,s,loopi):
    setwh=(not w==0) and (not h==0)
    if(setwh):
      cam.resolution=(w,h)
      
    cam.config.imageFX = cam.MMAL_PARAM_IMAGEFX_WATERCOLOUR
    cam.config.exposure = cam.MMAL_PARAM_EXPOSUREMODE_AUTO
    cam.config.meterMode = cam.MMAL_PARAM_EXPOSUREMETERINGMODE_AVERAGE
    cam.config.awbMode = cam.MMAL_PARAM_AWBMODE_SHADE
    cam.config.ISO = 0 #auto
    cam.config.ISO = 400
    cam.config.ISO = 800

    cam.config.sharpness = 0               # -100 to 100
    cam.config.contrast = 0                # -100 to 100
    cam.config.brightness = 50             #  0 to 100
    cam.config.saturation = 0              #  -100 to 100
    cam.config.videoStabilisation = 0      # 0 or 1 (false or true)
    cam.config.exposureCompensation  = 0   # -10 to +10 ?
    cam.config.rotation = 90               # 0-359
    cam.config.hflip = 1                   # 0 or 1
    cam.config.vflip = 0                   # 0 or 1
    cam.config.shutterSpeed = 20000         # 0 = auto, otherwise the shutter speed in ms

    cam.config.videoProfile = cam.MMAL_VIDEO_PROFILE_H264_HIGH
    cam.config.videoFramerate = 15
    cam.config.videoBitrate = 17000000

    cam.config.inlineHeaders = 0         # Insert inline headers to stream (SPS, PPS), 0 or 1
    cam.config.quantisationParameter = 0 # Quantisation parameter - quality. Set bitrate 0 and set this for variable bitrate

    cam.config.roi = [0.0,0.0,0.5,0.5]  # Region of interest, normalised coordinates (0.0 - 1.0).
    cam.config.roi = [0.5,0.5,0.25,0.25]

    cam.start_preview()
    #dirname="/var/www/image"   
    for i in range(loopi):   
      time.sleep(s)
      filename=name+"%02d" % i+ext
      filen=dirname+"/"+filename
      cam.capture(filen)
      #ShowImg(filen)
    cam.stop_preview()

def TakePhoto(dirname,name,ext,w,h,s,loopi):
    setwh=(not w==0) and (not h==0)
    for i in range(loopi):   
      time.sleep(s)
      filename=name+"%02d" % i+ext
      filen=dirname+"/"+filename
      if(setwh):
        pic=cam.takePhotoWithDetails(w,h,100)
      else:
        pic=cam.takePhoto()
      pic.save(filen)

def main(argv):
  w=640
  h=480
  s=0
  loopi=1
  dirf="image"
  try:
    opts, args=getopt.getopt(argv,"w:h:i:s:d:",["width=","height=","iloop=","sleep=","dir="])
  except:
     print(argv)
     
  for opt, arg in opts:
      if opt in ("-w","--width"):
        w=int(arg)
      elif opt in ("-h","--height"):
        h=int(arg)
      elif opt in ("-i","--iloop"):
        loopi=int(arg)
      elif opt in ("-s","--sleep"):
        s=int(arg)
      elif opt in ("-d","--dir"):
        dirf=arg
        
  dirname1="/var/www"+"/"+dirf
  print("<h1>",dirname1,"</h1>")
  name="Triggle"
  ext=".jpg"
  #ensure_dir(dirname1)
  #Triggle(dirname1,name,ext,w,h,s,loopi)
  #time.sleep(1)
  TakePhoto(dirname1,name,ext,w,h,s,loopi)
  ShowImgsWin(dirname1,name,ext,loopi)


if __name__ == "__main__":
   main(sys.argv[1:])

