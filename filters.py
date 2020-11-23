#http://datahacker.rs/004-how-to-smooth-and-sharpen-an-image-in-opencv/
import cv2
import numpy as np
##################Variables####################
hsv={
    "min_H":[0,180],
    "min_S":[0,255],
    "min_V":[0,255],
    "max_H":[180,180],
    "max_S":[255,255],
    "max_V":[255,255]
    }
#odd
meanFilter={
    "K_mean":[0,30]
    }
#odd
gaus={"K_gaus":[0,30],
    "Gaus_Std":[0,30]
    }
bilateral={"Diameter":[0,9],
    "Bil_Std":[0,300]}
erosion={"I_Ero":[0,20],"K_Ero":[0,20]}
dilation={"I_Dil":[0,20],"K_Dil":[0,20]}
opening={"K_Ope":[0,20]}
closing={"K_Clo":[0,20]}
gradient={"K_Grad":[0,20]}
laplacian={}
#K 1,3,5,7
sobelX={"K_SX":[0,3]}
sobelY={"K_SY":[0,3]}
filters={
    "hsv":hsv,"Mean":meanFilter,"Gaus":gaus,"Bil":bilateral,"Ero":erosion,
    "Dil":dilation,"Ope":opening,"Clos":closing,"Grad":gradient,"Lap":laplacian,
    "SoX":sobelX,"SoY":sobelY
    }
def on_off(fOp):
    return "OFF_ON:"+fOp

fb_T="Filter Options"

##################VariablesEND####################

#Created to use Trackbar
def nothing(x):
    pass

def crTraBar(Proper,Filter,Filters):
    fil=Filters[Filter]
    prop=fil[Proper]
    cv2.createTrackbar(Proper,fb_T,prop[0],prop[1],nothing)
def creatFilterBarsWindow():
    #### Create track bars
    cv2.namedWindow(fb_T)
    for filter in filters.keys():
        cv2.createTrackbar(on_off(filter),fb_T,0,1,nothing)
        for param in filters[filter].keys():
            crTraBar(param,filter,filters)
def readBars():
    ret={}
    for filter in filters.keys():
        ret[filter]={}
        ret[filter]["on"] = cv2.getTrackbarPos(on_off(filter),fb_T)
        for param in filters[filter].keys():
            ret[filter][param] = cv2.getTrackbarPos(param,fb_T)
    return ret
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
    "Ero":Erosion_filter,"Dil":Dilatation_filter,
    "Ope":Opening_Filter,"Clos":Closing_filter,
    "Grad":Gradient_filter,"Lap":Laplacian_filter,
    "SoX":SobelX_filter,"SoY":SobelY_filter,"hsv_mask":HSV_Mask}
def ordProcess(toWork,frame,param):
    if toWork=="hsv_mask":
        sendParam=param["hsv"]
    else:
        sendParam=param[toWork]
    return processes[toWork](frame,sendParam)
