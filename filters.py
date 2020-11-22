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
    "K_mean":[1,30]
    }
#odd
gaus={"K_gaus":[1,30],
    "Gaus_Std":[0,2]
    }
bilateral={"Diameter":[0,5],
    "Bil_Std":[0,100]}
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
    "SoX":sobelX,"sobelY":sobelY
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