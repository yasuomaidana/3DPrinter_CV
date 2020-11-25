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
videoName = "TrainVideos/WACHIS GG.avi"
cap = cv2.VideoCapture(videoName)

frame_width = int(cap.get(3))*2
frame_height = int(cap.get(4))

destName="To show/DetectObject.avi"
conFilter1=nV.loadData('To use/Mask.info')
conFilter2=nV.loadData('To use/Op1.info')
conFilter3=nV.loadData('To use/Op2.info')
#print(conFilter)
rec=False
nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
playSpeed = 50

cv2.namedWindow("To show")
cv2.createTrackbar("Frame", "To show", 0,nr_of_frames,getFrame)
cv2.createTrackbar("Speed", "To show", playSpeed,100,setSpeed)
def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])
def resize(img,scale_percent):
    #scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

while(1):   
    #Read a frame, ret indicates if the capture was succesful
    ret, frame = cap.read()
    if ret == True:
        ori=frame.copy() 
        mod1=filters.filfromConf(conFilter1,ori)
        mod2=filters.filfromConf(conFilter2,ori)
        mod3=filters.filfromConf(conFilter3,ori)
        sca=70
        ori = resize(ori,sca)
        mod1 = resize(mod1,sca)
        mod2 = resize(mod2,sca)
        mod3 = resize(mod3,sca)
        #show1 = cv2.hconcat([ori, mod1])
        #show2 = cv2.hconcat([mod2, mod3])
        cv2.imshow("To Original", ori)
        cv2.imshow("Masked", mod1)
        cv2.imshow("Analysis 1", mod2)
        cv2.imshow("Anaylisis", mod3)
            #out.write(frame)
        #except:
        #    neName=baseName+str(part)
        #    part+=1
        #    filePath=navFil.createFilePath(neName,'.avi','/media/pi/Yasuo/')
        #    out = cv2.VideoWriter(filePath,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        cv2.setTrackbarPos("Frame","Video", int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
    key = cv2.waitKey(playSpeed)
    
    if key==ord('q'):
        break
###########Stop recording
# When everything done, release the video capture and video write objects
cap.release()
