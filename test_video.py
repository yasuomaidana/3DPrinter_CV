import filters

import cv2
import numpy as np
import naviFiles as navFil




############################################################
############################################################
############################################################
# function called by trackbar, sets the next frame to be read

def getFrame(frame_nr):
    global video
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val,1)

filname=navFil.fileFromList('.avi')
filters.creatFilterBarsWindow()

# open video
video = cv2.VideoCapture(filname)
# get total number of frames
nr_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# create display window
cv2.namedWindow("Video")
# set wait for each frame, determines playbackspeed
playSpeed = 50
# add trackbar
cv2.createTrackbar("Frame", "Video", 0,nr_of_frames,getFrame)
cv2.createTrackbar("Speed", "Video", playSpeed,100,setSpeed)

############################################################
############################################################
############################################################

######   HSV #####
def readHSV(param):
    lH=param["min_H"]
    lS=param["min_S"]
    lV=param["min_V"]
    uH=param["max_H"]
    uS=param["max_S"]
    uV=param["max_V"]
    l_color = np.array([lH,lS,lV])
    u_color = np.array([uH,uS,uV])
    return l_color,u_color
def HSV_Masked(frame,param):
    if param["on"]==0:
        return frame
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        l_C,u_C=readHSV(param)
        mask = cv2.inRange(hsv,l_C,u_C)
        masked = cv2.bitwise_and(frame, frame, mask = mask)
        return masked
def HSV_Mask(frame,param):
    if param["on"]==0:
        return frame
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        l_C,u_C=readHSV(param)
        mask = cv2.inRange(hsv,l_C,u_C)
        return mask
######HSV end #####
######  Mean #####
def Mean_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_mean"]
        k=k*2+1
        median = cv2.medianBlur(frame,k)
        return median
####Mean end #####
######  Gaus #####
def Gaussian_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_gaus"]
        k=k*2+1 
        std=param["Gaus_Std"]
        std=std*2+1
        gaus = cv2.GaussianBlur(frame,(std,std),k)
        return gaus
####Gaus end #####
######  Bilateral #####
def Bilateral_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        d=param["Diameter"]
        
        std=param["Bil_Std"]
        
        bil = cv2.bilateralFilter(frame,d,std,std)
        return bil
####Bilateral end #####

#####Morfological
##
#####
def genKer(Ks):
    return np.ones((Ks,Ks),np.uint8)
    
######  Erosion #####
def Erosion_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_Ero"]
        k+=1
        Kernel=genKer(k)
        I=param["I_Ero"]
        ero = cv2.erode(frame,Kernel,iterations = I)
        return ero
####Erosion end #####

#Dilation
def Dilatation_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_Dil"]
        k+=1
        Kernel=genKer(k)
        I=param["I_Dil"]
        dil = cv2.dilate(frame,Kernel,iterations = I)
        return dil
######  Dilation #####
####Dilation end #####
#Opening
def Opening_Filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_Ope"]
        k+=1
        kernel=genKer(k)
        opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        return opening
######  Opening #####
####Opening end #####
#Closing
######  Closing #####
def Closing_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_Clo"]
        k+=1
        kernel=genKer(k)
        closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
        return closing
####Closing end #####
#Gradient
######  Gradient #####
def Gradient_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_Grad"]
        k+=1
        kernel=genKer(k)
        gradient = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
        return gradient
####Gradient end #####

#####
##
#####MorfologicalEnd

#Laplacian
######  Laplacian #####
def Laplacian_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        lap=cv2.Laplacian(frame,cv2.CV_64F)
        return lap
####Laplacian end #####
#Sobel "SoX":sobelX,"sobelY":sobelY
######  Sobel #####

def Sobel_filter(frame,kS,op):
    sobel = cv2.Sobel(frame,cv2.CV_64F,op[0],op[1],ksize=kS)
    return sobel
def SobelX_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_SX"]
        k=2*k+1
        op=[1,0]
        sobelx=Sobel_filter(frame,k,op)
        return sobelx
def SobelY_filter(frame,param):
    if param["on"]==0:
        return frame
    else:
        k=param["K_SY"]
        k=2*k+1
        op=[0,1]
        sobely=Sobel_filter(frame,k,op)
        return sobely
####Sobel end #####

processes={
    "hsv":HSV_Masked,"Mean":Mean_filter,
    "Gaus":Gaussian_filter,"Bil":Bilateral_filter,
    "Ero":Erosion_filter,"Dil":Erosion_filter,
    "Ope":Opening_Filter,"Clos":Closing_filter,
    "Grad":Gradient_filter,"Lap":Laplacian_filter,
    "SoX":SobelX_filter,"SoY":SobelY_filter}
def ordProcess(toWork,frame,param):
    sendParam=param[toWork]
    return processes[toWork](frame,sendParam)

while 1:
    ret, frame = video.read()

    # show frame, break the loop if no frame is found
    if ret:
        cv2.imshow("Video", frame)
        param=filters.readBars()
        modi=ordProcess("Mean",frame,param)
        modi=ordProcess("Gaus",modi,param)
        modi=ordProcess("Bil",modi,param)
        
        modi=ordProcess("hsv",modi,param)
        modi=filters.ordProcess("Dil",modi,param)
        modi=ordProcess("Ero",modi,param)
        modi=ordProcess("Ope",modi,param)
        modi=ordProcess("Clos",modi,param)
        modi=ordProcess("Grad",modi,param)
        modi=ordProcess("Lap",modi,param)
        modi=ordProcess("SoX",modi,param)
        modi=ordProcess("SoY",modi,param)
        cv2.imshow("Processed", modi)

        
        # update slider position on trackbar
        # NOTE: this is an expensive operation, remove to greatly increase max playback speed
        cv2.setTrackbarPos("Frame","Video", int(video.get(cv2.CAP_PROP_POS_FRAMES)))
    else:
        break

    key = cv2.waitKey(playSpeed)

    # stop playback when q is pressed
    if key == ord('q'):
        print(filters.readBars())
        break