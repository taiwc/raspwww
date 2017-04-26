# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 08:34:58 2017

@author: ASUS
"""
import numpy as np
import time
import sys, getopt
import io
import picamera
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
        
def ShowImg(filen):
      showcmd="file_viewerNoCode.php?file="+filen+"";
      strmsg="<img src=\""+showcmd+"\""+" alt='"+filen+"' />"
      print(strmsg);

def ShowImgs(dirname,name,ext,loopi):
    for i in range(loopi):
        filen=dirname+"/"+name+"%02d"%i+ext
        ShowImg(filen)
      
def Triggle(dirname,name,ext,w,h,s,loopi):
  with picamera.PiCamera() as camera:
    setwh=(not w==0) and (not h==0)
    if(setwh):
      camera.resolution=(w,h)

    camera.start_preview()
    #dirname="/var/www/image"   
    for i in range(loopi):   
      time.sleep(s)
      filename=name+"%02d" % i+ext
      filen=dirname+"/"+filename
      camera.capture(filen)
      #ShowImg(filen)
    camera.stop_preview()

def TakePhoto(dirname,name,ext,w,h,s,loopi):
  with picamera.PiCamera() as camera:
    setwh=(not w==0) and (not h==0)
    for i in range(loopi):   
      time.sleep(s)
      filename=name+"%02d" % i+ext
      filen=dirname+"/"+filename
      if(setwh):
        pic=camera.takeRGBPhotoWithDetails(w,h)
      else:
        pic=camera.takePhoto()
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
  Triggle(dirname1,name,ext,w,h,s,loopi)
  #time.sleep(1)
  #TakePhoto(dirname,name,ext,w,h,s,loopi)
  ShowImgs(dirname1,name,ext,loopi)


if __name__ == "__main__":
   main(sys.argv[1:])
