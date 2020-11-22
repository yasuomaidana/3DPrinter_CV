import cv2
import numpy as np

##Miscelaneous
import naviFiles as navFil
#X:94.00 Y:-52.00 Z:159.00 E:0.00

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

#############Function to create HSV manipulator stuffs
trName= "Track bars HSV format"

#Created to use Trackbar
def nothing(x):
    pass
#Calibration calls bars values
def cali():
    # Obtain HSV values to create mask
    l_h = cv2.getTrackbarPos("Low-H",trName)
    l_s = cv2.getTrackbarPos("Low-S",trName)
    l_v = cv2.getTrackbarPos("Low-V",trName)
    u_h = cv2.getTrackbarPos("High-H",trName)
    u_s = cv2.getTrackbarPos("High-S",trName)
    u_v = cv2.getTrackbarPos("High-V",trName)

    # Create levels arrays
    l_color = np.array([l_h,l_s,l_v])
    u_color = np.array([u_h,u_s,u_v])

    #Obtain kernel size
    ks = cv2.getTrackbarPos("KS","Kernel Size")

    return [l_color, u_color,ks]

#Creates bars to obtain HSV values
def creatBar():
    #### Create track bars
    cv2.namedWindow(trName)
    ## Low HSV level
    cv2.createTrackbar("Low-H",trName,0,180,nothing)
    cv2.createTrackbar("Low-S",trName,0,255,nothing)
    cv2.createTrackbar("Low-V",trName,0,255,nothing)
    ## High HSV level
    cv2.createTrackbar("High-H",trName,180,180,nothing)
    cv2.createTrackbar("High-S",trName,255,255,nothing)
    cv2.createTrackbar("High-V",trName,255,255,nothing)
    ### Create track bars end

    ##Bar to get kernel
    cv2.namedWindow("Kernel Size")
    cv2.createTrackbar("KS","Kernel Size",0,255,nothing)
###########end of HSV manipulator stuffs
#Obtains the mask used for obtain the color cells
def Obtain_Mask(frame):
    #creatBar()
    #while(True): 
        # Capture frame-by-frame
    #_, frame = cap.read()
        #Convert mask to HSV format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #if cal:
    [l_color, u_color,ks] = cali()
    #else:
        #[l_color, u_color,ks] = noCali()

        #Create mask 
    mask = cv2.inRange(hsv,l_color,u_color)

        #Erode mask
    kernel = np.ones((ks,ks),np.uint8)
    mask = cv2.erode(mask,kernel)
        #Dilatation
    mask = cv2.dilate(mask, kernel)
    
    cv2.imshow('Mask',mask)
# main loop
creatBar()
while 1:
    # Get the next videoframe
    ret, frame = video.read()

    # show frame, break the loop if no frame is found
    if ret:
        cv2.imshow("Video", frame)
        # update slider position on trackbar
        # NOTE: this is an expensive operation, remove to greatly increase max playback speed
        cv2.setTrackbarPos("Frame","Video", int(video.get(cv2.CAP_PROP_POS_FRAMES)))
    else:
        break

    
    Obtain_Mask(frame)
    # display frame for 'playSpeed' ms, detect key input
    key = cv2.waitKey(playSpeed)

    # stop playback when q is pressed
    if key == ord('q'):
        break

# release resources
video.release()
cv2.destroyAllWindows()