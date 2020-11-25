#This program prints an object while record the printing video

#This lines are needed in order to allow the program to access to Printrun library
import sys
sys.path.append('/home/pi/Printrun')

#Load printrun objects
#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder

#Load OpenCV library
import cv2

#Import miscelaneous libraries
import numpy as np
import os.path
from os import path
import naviFiles as navFil

###########################
###----FUNCTIONS END----###
###########################

#####################
###Printing code part
#Made comunication with 3D printer
p=printcore('/dev/ttyUSB0',115200) # or p.printcore('COM3',115200) on Windows

filename=navFil.fileFromList('.gcode','/home/pi/Desktop/')
#filePath='/home/pi/Desktop/'+filename+'.gcode'
#Split the code into a list
gcode=[i.strip() for i in open(filename)] # or pass in your own array of gcode lines instead of reading from a file
#Transform the previous list into an object, this object has some properties to allow the printing process
gcode = gcoder.LightGCode(gcode)
########end of printing part
###################

#################
###Video preparation code part
# Create a VideoCapture object
cap = cv2.VideoCapture(0)
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
# Default resolutions of the frame are obtained.The default resolutions are system dependent
# We convert the resolutions from float to integer
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


filename,_=navFil.getNameFromPath(filename)
filePath=navFil.createFilePath(filename,'.avi','/media/pi/Yasuo/')
baseName=navFil.getNameFromPath(filePath)

###



p.connect()
p.send("G1 X99.00 Y219.00 Z165.00")
p.send_now("G1 X99.00 Y219.00 Z165.00")
p.startprint(gcode) # this will start a print

i=0
part=2
#while(p.printing):
while(p.printing):   
    #Read a frame, ret indicates if the capture was succesful
    ret, frame = cap.read()
    if ret == True: 
        try :
            # Write the frame into the file 'output.avi'
            out.write(frame)
        except:
            neName=baseName+str(part)
            part+=1
            filePath=navFil.createFilePath(neName,'.avi','/media/pi/Yasuo/')
            out = cv2.VideoWriter(filePath,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        # Display the resulting frame    
    if i%1000==0:
        #If you send a lot of instructions you will stop the prining process
        #p.send_now("M105")
        progress = 100 * float(p.queueindex) / len(p.mainqueue)
        print(progress)
        #try:
        #    a=p._readline()
        #    
        #except:
        #    a=""
        #print(a)
        i=0
    else:
        i+=1
###########Stop recording
# When everything done, release the video capture and video write objects
cap.release()
out.release()
# Closes all the frames
#cv2.destroyAllWindows() 
###########end stop recording

#If you need to interact with the printer:
#p.cancelprint() # this will send M105 immediately, ahead of the rest of the print

#p.pause() # use these to pause/resume the current print
#p.resume()
p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.


print("done")
print("Lost frames :"+str(lost))