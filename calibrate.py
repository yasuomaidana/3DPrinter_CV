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

filname=navFil.fileFromList('.avi','TrainVideos/')

filter_ord=men2()

# open video
video = cv2.VideoCapture(filname)

filters.creatFilterBarsWindow()

# get total number of frames
nr_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# create display window
cv2.namedWindow("Video")
# set wait for each frame, determines playbackspeed
playSpeed = 50
# add trackbar
cv2.createTrackbar("Frame", "Video", 0,nr_of_frames,getFrame)
cv2.createTrackbar("Speed", "Video", playSpeed,100,setSpeed)

filters_names=[
    "hsv","hsv_mask",
    "Mean","Gaus",
    "Bil","Grad","Lap","SoX","SoY",
    "Ero","Dil","Ope","Clos"
    ]

defaultOrd=[
    "hsv","Mean","Gaus","Bil","Ero","Dil","Ope",
    "Clos","Grad","Lap","SoX","SoY"]

def noLoad(frame,params):
    c=0
    for i in defaultOrd:
        if c==0:
            c+=1
            modi=filters.ordProcess(i,frame,param)
        else:
            modi=filters.ordProcess(i,modi,param)
    return modi
con=True
ret, frame = video.read()
while 1:
    
    if con:
        ret, frame = video.read()
    # show frame, break the loop if no frame is found
    if ret:
        cv2.imshow("Video", frame)
        param=filters.readBars()
        if len(filter_ord)==0:
            modi=noLoad(frame,param)
        else:
            modi=frame
            modi=filters.filfromConf(filter_ord,modi)
            modi=noLoad(modi,param)
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
        filter_ord=navFil.saveData(dat,getUsed(param),filter_ord)
        eS=True
        while eS:
            key = cv2.waitKey(playSpeed)
            if key == ord('c'):
                eS=False
    # stop playback when q is pressed
    if key == ord('q'):
        sav=input("Do you want to save this configuration? \n Yes (1) No(0) :")
        if sav:
            pic,dat=navFil.incName()
            cv2.imwrite(pic,modi)
        
            navFil.saveData(dat,getUsed(param),filter_ord)
        
        #usedNames=navFil.getFilesbyType('.png','FilterOp')
        
        break
