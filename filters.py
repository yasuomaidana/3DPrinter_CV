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
Gray_Scale={"L_Thres":[0,255],"U_Thres":[255,255],"Mode":[0,4]}
filters={
    "hsv":hsv,"Mean":meanFilter,"Gaus":gaus,"Bil":bilateral,"Ero":erosion,
    "Dil":dilation,"Ope":opening,"Clos":closing,"Grad":gradient,"Lap":laplacian,
    "SoX":sobelX,"SoY":sobelY
    }


#wrOP={"Mask_Prev_Or":[0,1]}
masks={"GrS":Gray_Scale,"hsv_mask":{},"NotF":{},"AndF":{},"OrF":{},"XORF":{},"WrO":{}}
def on_off(fOp):
    return "OFF_ON:"+fOp

##################VariablesEND####################

#Created to use Trackbar
def nothing(x):
    pass

def crTraBar(Proper,Filter,Filters,fb_T):
    fil=Filters[Filter]
    prop=fil[Proper]
    cv2.createTrackbar(Proper,fb_T,prop[0],prop[1],nothing)
def creatFilterBarsWindow(fb_T,filters):
    #### Create track bars
    cv2.namedWindow(fb_T)
    for filter in filters.keys():
        cv2.createTrackbar(on_off(filter),fb_T,0,1,nothing)
        for param in filters[filter].keys():
            crTraBar(param,filter,filters,fb_T)
def readBars(fb_T,filters):
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

####################################
##### Masks
####################################
#{'GrS': {'on': 0, 'L_Thres': 25, 'U_Thres': 255, 'Mode': 0},
# 'hsv_mask': {'on': 0},
# not:{} 
# 'And': {'on': 0}, 
# 'Or': {'on': 0}, 
# 'XOR': {'on': 0}, 
# 'Show': {'on': 1, 'Mask_Prev_Or': 0}}
def HSV_Mask(frame,maskParam,param,ori=None):
    param2=maskParam["hsv_mask"]
    if param2["on"]==0:
        return frame
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        l_C,u_C=readHSV(param["hsv"])
        mask = cv2.inRange(hsv,l_C,u_C)
        return mask

def GrayScale(frame,maskParam,param=None,ori=None):
    param=maskParam["GrS"]
    if param["on"]==0:
        return frame
    else:
        Mode=[
        cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV,
        cv2.THRESH_TRUNC,cv2.THRESH_TOZERO,
        cv2.THRESH_TOZERO_INV]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _,mask = cv2.threshold(gray, param["L_Thres"], param["U_Thres"], Mode[param["Mode"]]) 
        return mask
def notFilter(frame,maskParam,param=None,ori=None):
    param=maskParam["NotF"]
    if param["on"]==0:
        return frame
    else:
        mask = cv2.bitwise_not(frame) 
        return mask


#masks=["AndF","OrF","XORF"]
maskG=["GrS","hsv_mask"]#,"NotF"]
maskP=["AndF","OrF","XORF","GrS","hsv_mask","NotF"]
def selMask(maskParam):
    paramG=maskParam["GrS"]
    paramH=maskParam["hsv_mask"]
    r=False
    mask1=notFilter
    if paramG["on"]:
        r=True
        mask1=GrayScale
        return r,mask1
    if paramH["on"]:
        r=True
        mask1=HSV_Mask
        return r,mask1
    return r,mask1
#processes[toWork](frame,maskParam,param,ori)

def andFilter(frame,maskParam,param=None,ori=None):
    param2=maskParam["AndF"]
    
    if param2["on"]==0:
        
        return frame
    else:
        d,dM=selMask(maskParam)
        
        if d:
            mask=dM(frame,maskParam,param,ori)
            mask=notFilter(mask,maskParam,param,ori)
                
            if maskParam["WrO"]:
                
                blue, green, red = cv2.split(ori)
                blue = cv2.bitwise_and(blue,mask)
                green = cv2.bitwise_and(green,mask)
                red = cv2.bitwise_and(red,mask)
                     
            else:
                
                blue, green, red = cv2.split(frame)
                blue = cv2.bitwise_and(blue,mask)
                green = cv2.bitwise_and(green,mask)
                red = cv2.bitwise_and(red,mask)
                
            masked = cv2.merge((blue,green,red))
            return masked
        else:
            return frame
def orFilter(frame,maskParam,param=None,ori=None):
    param2=maskParam["OrF"]
    if param2["on"]==0:
        
        return frame
    else:
        d,dM=selMask(maskParam)
        
        if d:
            mask=dM(frame,maskParam,param,ori)
            mask=notFilter(mask,maskParam,param,ori)
            if maskParam["WrO"]:
                
                blue, green, red = cv2.split(ori)
                blue = cv2.bitwise_or(blue,mask)
                green = cv2.bitwise_or(green,mask)
                red = cv2.bitwise_or(red,mask)
                     
            else:
                
                blue, green, red = cv2.split(frame)
                blue = cv2.bitwise_or(blue,mask)
                green = cv2.bitwise_or(green,mask)
                red = cv2.bitwise_or(red,mask)
                
            masked = cv2.merge((blue,green,red))
            return masked
        else:
            return frame
def xorFilter(frame,maskParam,param=None,ori=None):
    param2=maskParam["XORF"]
    if param2["on"]==0:
        
        return frame
    else:
        d,dM=selMask(maskParam)
        
        if d:
            mask=dM(frame,maskParam,param,ori)
            mask=notFilter(mask,maskParam,param,ori)
                
            if maskParam["WrO"]:
                blue, green, red = cv2.split(frame)
                blue = cv2.bitwise_xor(blue,mask)
                green = cv2.bitwise_xor(green,mask)
                red = cv2.bitwise_xor(red,mask)
                     
            else:
                blue, green, red = cv2.split(ori)
                blue = cv2.bitwise_xor(blue,mask)
                green = cv2.bitwise_xor(green,mask)
                red = cv2.bitwise_xor(red,mask)
                
            masked = cv2.merge((blue,green,red))
            return masked
        else:
            return frame


####################################
##### Masks end
####################################

processes={
    "hsv":HSV_Masked,"GrS":GrayScale,"Mean":Mean_filter,
    "Gaus":Gaussian_filter,"Bil":Bilateral_filter,
    "Ero":Erosion_filter,"Dil":Dilatation_filter,
    "Ope":Opening_Filter,"Clos":Closing_filter,
    "Grad":Gradient_filter,"Lap":Laplacian_filter,
    "SoX":SobelX_filter,"SoY":SobelY_filter,
    "hsv_mask":HSV_Mask,"AndF":andFilter,
    "NotF":notFilter,"OrF":orFilter,"XORF":xorFilter}
def ordProcess(toWork,frame,param,ori=None,maskParam=None):
    if toWork in maskP:
        #cv2.imshow("PreFilter", frame)
        #cv2.imshow("Origi", ori)
        return processes[toWork](frame,maskParam,param,ori)
    if toWork=="Show":
        return frame
    
    sendParam=param[toWork]
    
    return processes[toWork](frame,sendParam)

defaultOrd=[
    "Mean","Gaus","Bil","Ero","Dil","Ope",
    "Clos","Grad","Lap","SoX","SoY","hsv"]
defaultOrd2=["hsv_mask","GrS","NotF","AndF","OrF","XORF"]

defaultOrd2=["hsv_mask","GrS","NotF","AndF","OrF","XORF"]
def runMask(frame,params,ori,maskParams):
    spec=False
    for i in defaultOrd2:
        ind=defaultOrd2.index(i) 
        if(maskParams[i]["on"] and ind>2):
            spec=True
            break
    if spec:
        return ordProcess(defaultOrd2[ind],frame,params,ori,maskParams)
    else:
        ind=0
        modi=frame
        for i in defaultOrd2:
            ordProcess(i,modi,params,ori,maskParams)
            if ind>2:
                break
            ind+=1
    return modi

def filfromConf(confi,modi):
    ori=modi.copy()
    #print(confi)
    for step in confi:        
        if 'm' in step :
            param=confi[step]['F']
            param2=confi[step]['M']
            modi = runMask(modi,param,ori,param2)
        else:
            for fil in confi[step]:
                modi=ordProcess(fil,modi,confi[step],ori)
    return modi
