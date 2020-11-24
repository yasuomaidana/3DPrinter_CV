import filters

import cv2
import numpy as np
import naviFiles as navFil


############################################################
# function called by trackbar, sets the next frame to be read

def getFrame(frame_nr):
    global video
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val,1)
###############################################################
############################################################
def getUsed(params):
    used={}
    for par in params.keys():
        if params[par]["on"]:
            used[par]=params[par]
    return used

filters_names=[
    "hsv","hsv_mask",
    "Mean","Gaus",
    "Bil","Grad","Lap","SoX","SoY",
    "Ero","Dil","Ope","Clos"
    ]
def men():
    print("Filters used to color filtering")
    for i in filters_names[0:2]:
        print(i)
    print("Filters used to smooth")
    for i in filters_names[2:4]:
        print(i)
    print("Filters used to sharp")
    for i in filters_names[4:9]:
        print(i)
    print("Filters used for morphological trans")
    for i in filters_names[9:]:
        print(i)

def men2():
    l=input("Do you want to start from previous configuration? \n(1) yes (0) no: ")
    r={}
    if int(l):
        stConf=navFil.fileFromList('.info','FilterOp/')
        r=navFil.loadData(stConf)
    return r
############################################################
men()
filname=navFil.fileFromList('.avi','TrainVideos/')

filter_ord=men2()

# open video
video = cv2.VideoCapture(filname)

filters.creatFilterBarsWindow("Masks options",filters.masks)
filters.creatFilterBarsWindow("Filter Options",filters.filters)
cv2.namedWindow("Filter Options", cv2.WINDOW_NORMAL)

# get total number of frames
nr_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# create display window
cv2.namedWindow("Video")
# set wait for each frame, determines playbackspeed
playSpeed = 50
# add trackbar
cv2.createTrackbar("Frame", "Video", 0,nr_of_frames,getFrame)
cv2.createTrackbar("Speed", "Video", playSpeed,100,setSpeed)



defaultOrd=[
    "Mean","Gaus","Bil","Ero","Dil","Ope",
    "Clos","Grad","Lap","SoX","SoY","hsv"]
def noLoad(frame,params):
    c=0
    for i in defaultOrd:
        if c==0:
            c+=1
            modi=filters.ordProcess(i,frame,params)
        else:
            modi=filters.ordProcess(i,modi,params)
    return modi
defaultOrd2=["hsv_mask","GrS","NotF","AndF","OrF","XORF"]
def noLoad2(frame,params,ori,maskParams):
    spec=False
    for i in defaultOrd2:
        ind=defaultOrd2.index(i) 
        if(maskParams[i]["on"] and ind>2):
            spec=True
            break
    if spec:
        return filters.ordProcess(defaultOrd2[ind],frame,param,ori,maskParams)
    else:
        ind=0
        modi=frame
        for i in defaultOrd2:
            modi=filters.ordProcess(i,modi,param,ori,maskParams)
            if ind>2:
                break
            ind+=1
    return modi


def comb(param,param2):
    ma=False
    for m in param2.keys():
        if param2[m]['on']==1:
            ma=True
            break
    if not ma:
        return None
    r={}
    r['F']=param
    r['M']=param2
    return r
con=True
ret, frame = video.read()
while 1:
    ori=frame.copy()
    if con:
        ret, frame = video.read()
    # show frame, break the loop if no frame is found
    if ret:
        cv2.imshow("Video", frame)
        param=filters.readBars("Filter Options",filters.filters)
        param2=filters.readBars("Masks options",filters.masks)
        if len(filter_ord)==0:
            modi=noLoad(frame,param)
            modi=noLoad2(modi,param,ori,param2)
        else:
            modi=filters.filfromConf(filter_ord,frame)
            modi=noLoad(modi,param)
            modi=noLoad2(modi,param,ori,param2)
        cv2.imshow("Processed", modi)
        
        # update slider position on trackbar
        # NOTE: this is an expensive operation, remove to greatly increase max playback speed
        
        cv2.setTrackbarPos("Frame","Video", int(video.get(cv2.CAP_PROP_POS_FRAMES)))
    else:
        break
    
    key = cv2.waitKey(playSpeed)
    if key==ord('p'):
        con=False
    if key==ord('c'):
        con=True
    if key == ord('s'):
        pic,dat=navFil.incName()
        cv2.imwrite(pic,modi)
        
        Mseq=comb(param,param2)
        print(Mseq)
        filter_ord=navFil.saveData(dat,getUsed(param),filter_ord,Mseq)
        eS=True
        while eS:
            key = cv2.waitKey(playSpeed)
            if key == ord('c'):
                eS=False
    # stop playback when q is pressed
    if key == ord('q'):
        #param2=prepSaV(param2)
        Mseq=comb(param,param2)
        print(Mseq)
        cv2.destroyAllWindows()
        #cv2.destroyWindow("shown_img")
        sav=int(input("Do you want to save this configuration? \n Yes (1) No(0) :"))
        if sav:
            pic,dat=navFil.incName()
            cv2.imwrite(pic,modi)
            filter_ord=navFil.saveData(dat,getUsed(param),filter_ord,Mseq)
        break
