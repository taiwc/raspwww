# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 07:55:58 2017

@author: ASUS
"""

import numpy as np
import cv2
import glob
import sys
import getopt
import os
#import urllib2

def savetxtMsg(rootpath,dirname,fname,msg,data):
  ff=dirname+'/'+fname
  np.savetxt(rootpath+'/'+ff,data)
  printrefMsg(ff,ff,msg)  

def printref(refpath,refprn):
  print("<a href=",refpath,">")
  print(refprn)
  print("</a>")

def printrefMsg(refpath,refprn,msg):
  print("<h1>")
  printref(refpath,refprn)
  print(msg)
  print("</h>")
    
def cv2chess(row,col,gsize,rootpath,dirname,ffilter):        
  #row=9
  #col=6
  #gsize=20 #mm
  #filefilter='Triggle??.jpg'
  # termination criteria
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
  # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
  objp = np.zeros((col*row,3), np.float32)
  objp[:,:2] = np.mgrid[0:row,0:col].T.reshape(-1,2)
  objp[:,:2] = objp[:,:2]*gsize
  #savetxtMsg(rootpath,dirname,"ObjPoint.txt"," 3d point ",objp) 
  # Arrays to store object points and image points from all the images.
  objpoints = [] # 3d point in real world space
  imgpoints = [] # 2d points in image plane.
  filefilter=rootpath+'/'+dirname+'/'+ffilter
  images = glob.glob(filefilter)
  i=0
  chsdirref=dirname+'/'+'ChessImg'
  #chsdir=rootpath+'/'+dirname+'/'+'ChessImg'
  for fname in images:
    bname=os.path.basename(fname)
    refname=dirname+'/'+bname
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('img',img)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (row,col),None)
    # If found, add object points, image points (after refining them)
    if ret == True:
      printrefMsg(refname,refname," Chess Ok!")     
      objpoints.append(objp)
      corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
      #savetxtMsg(rootpath,dirname,bname+".2d.txt"," 2d point ",corners2)     
      imgpoints.append(corners2)
      # Draw and display the corners
      imgchess = cv2.drawChessboardCorners(img, (row,col), corners2,ret)
      chsfname=chsdirref+'/'+('Chess%02d.jpg' % i)
      cv2.imwrite(rootpath+'/'+chsfname,imgchess)
      printrefMsg(chsfname,chsfname," draw corner")  
      i=i+1
      #cv2.imshow('imgchess',imgchess)
      #cv2.waitKey(500)
    else:
      printrefMsg(refname,refname," Chess Failed!")

  #Camera Calibration
  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],None,None)
  ##find the rotation and translation vector
  savetxtMsg(rootpath,dirname,"rvecs.txt"," rotation vectors",rvecs)
  savetxtMsg(rootpath,dirname,"tvecs.txt"," translation vectors",tvecs)
  savetxtMsg(rootpath,dirname,"mtx.txt"," transform matrix",mtx)
  savetxtMsg(rootpath,dirname,"dist.txt"," distortion coeffience",dist)
  
  objf=dirname+'/'+"objpoints"
  np.savez(rootpath+'/'+objf,*objpoints)
  printrefMsg(objf+".npz",objf+".npz"," coordinate 3d data")
  imgf=dirname+'/'+"imgpoints"
  np.savez(rootpath+'/'+imgf,*imgpoints)
  printrefMsg(imgf+".npz",imgf+".npz"," image 2d point")
  # undistort
  h,w=img.shape[:2]
  newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
  savetxtMsg(rootpath,dirname,"newcameramtx.txt"," new camera matrix",newcameramtx)
  
  #roif=dirname+'/'+"roi.txt"
  #np.savetxt(rootpath+'/'+roif,roi)
  #printrefMsg(roif,roif," Range Of Inspection")
  savetxtMsg(rootpath,dirname,"roi.txt"," range of inspection",roi)
  
  #print("M1=",newcameramtx)
  #print("ROI=",roi)
  err=CheckError(imgpoints,objpoints,rvecs,tvecs,mtx,dist)
  print("<h1> Error=",err,"</h>")

def LoadCalibrationFileData(dirname):
  rvecs=np.loadtxt(dirname+'/'+"rvecs.txt")
  tvecs=np.loadtxt(dirname+'/'+"tvecs.txt")
  mtx=np.loadtxt(dirname+'/'+"mtx.txt")
  dist=np.loadtxt(dirname+'/'+"dist.txt") 
  return rvecs,tvecs,mtx,dist

def UndistoreImgFile(fname,mtx,dist,fnameout): 
    img=cv2.imread(fname)
    h,w=img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    dst=cv2.undistort(img,mtx,dist,None,newcameramtx)
    #x,y,w,h=roi
    #dst=dst[y:y+h,x:x+w]
    cv2.imwrite(fnameout,dst)
    return dst

def UndistoreImg(dirname,ffilter,mtx,dist):        
  filefilter=dirname+'/'+ffilter
  images = glob.glob(filefilter)
  i=0
  undir=dirname+'/'+'UndistImg'
  for fname in images:
    UndistoreImgFile(fname,mtx,dist,undir+'/'+"undist%02d.jpg"%i)
    i=i+1
      
def CheckError(imgpoints,objpoints,rvecs,tvecs,mtx,dist):
  mean_error=0
  tot_error=0
  for i in range(len(objpoints)):
    imgpoints2, _=cv2.projectPoints(objpoints[i],rvecs[i],tvecs[i],mtx,dist)
    error=cv2.norm(imgpoints[i],imgpoints2,cv2.NORM_L2)/len(imgpoints2)
    tot_error+=error

  meanerror=tot_error/len(objpoints)  
  return meanerror
      
def CountError(dirname):
  rvecs=np.loadtxt(dirname+'/'+"rvecs.txt")
  tvecs=np.loadtxt(dirname+'/'+"tvecs.txt")
  mtx=np.loadtxt(dirname+'/'+"mtx.txt")
  dist=np.loadtxt(dirname+'/'+"dist.txt")
  objpoints=np.load(dirname+'/'+"objpoints.npz")
  imgpoints=np.load(dirname+'/'+"imgpoints.npz")
  meanerror=CheckError(imgpoints.files,objpoints.files,rvecs,tvecs,mtx,dist)
  print("mean error:",meanerror)

def main(argv):
  rootpath="/var/www"
  dirf="Calibration"
  ffilter="Triggle??.jpg"
  row=9
  col=6
  grid=20 #mm
  try:
    opts, args=getopt.getopt(argv,"r:c:g:d:f:",["row=","col=","grid=","dir=","filter="])
  except:
     print(argv)
     
  for opt, arg in opts:
      if opt in ("-r","--row"):
        row=int(arg)
      elif opt in ("-c","--col"):
        col=int(arg)
      elif opt in ("-g","--grid"):
        grid=float(arg)
      elif opt in ("-d","--dir"):
        dirf=arg
      elif opt in ("-f","--filter"):
        ffilter=arg
  
  dirname1=dirf
  cv2chess(row,col,grid,rootpath,dirname1,ffilter)
  rvecs,tvecs,mtx,dist=LoadCalibrationFileData(rootpath+'/'+dirname1)
  UndistoreImg(rootpath+'/'+dirname1,ffilter,mtx,dist)
  #CountError(dirf)

if __name__ == "__main__":
   main(sys.argv[1:])

#cv2.destroyAllWindows()
