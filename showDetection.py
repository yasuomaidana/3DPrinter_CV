import naviFiles as nV
import filters

from filters import runMask as rM
from filters import ordProcess as oP
import cv2


############################################################
# function called by trackbar, sets the next frame to be read

def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val,1)

####################################


#Load video
videoName = "TrainVideos/calibrate A.avi"
cap = cv2.VideoCapture(videoName)

frame_width = int(cap.get(3))*2
frame_height = int(cap.get(4))

destName="To show/DetectObject.avi"
conFilter=nV.loadData('To use/DetectInside.info')
#print(conFilter)
rec=False
nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
playSpeed = 50

cv2.namedWindow("To show")
cv2.createTrackbar("Frame", "To show", 0,nr_of_frames,getFrame)
cv2.createTrackbar("Speed", "To show", playSpeed,100,setSpeed)
while(1):   
    #Read a frame, ret indicates if the capture was succesful
    ret, frame = cap.read()
    if ret == True: 
        ori=frame.copy()
        modi=frame
        
        for step in conFilter:
            #for i in range(0,10):        
            if 'm' in step :
                param=conFilter[step]['F']
                param2=conFilter[step]['M']
                modi = rM(modi,param,ori,param2)
                
            else:
                for fil in conFilter[step]:
                    modi=oP(fil,modi,conFilter[step],ori)
                    
        show = cv2.hconcat([ori, modi])
        cv2.setTrackbarPos("Frame","Video", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        cv2.imshow("To show", show)
        #out.write(frame)
        #except:
        #    neName=baseName+str(part)
        #    part+=1
        #    filePath=navFil.createFilePath(neName,'.avi','/media/pi/Yasuo/')
        #    out = cv2.VideoWriter(filePath,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    
    key = cv2.waitKey(playSpeed)
    
    if key==ord('q'):
        break
    
###########Stop recording
# When everything done, release the video capture and video write objects
cap.release()
