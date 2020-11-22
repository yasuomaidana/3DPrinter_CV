import filters

import cv2
import numpy as np
import naviFiles as navFil
filters.creatFilterBarsWindow()
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
processes={"hsv":HSV_Masked}
def ordProcess(toWork,frame,param):
    sendParam=param[toWork]
    return processes[toWork](frame,sendParam)

while 1:
    ret, frame = video.read()

    

    # show frame, break the loop if no frame is found
    if ret:
        cv2.imshow("Video", frame)
        param=filters.readBars()
        
        modi=ordProcess("hsv",frame,param)
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
