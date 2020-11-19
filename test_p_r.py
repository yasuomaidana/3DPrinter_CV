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


#Made comunication with 3D printer
p=printcore('/dev/ttyUSB0',115200) # or p.printcore('COM3',115200) on Windows
#Split the code into a list
gcode=[i.strip() for i in open('AA8_calicat.gcode')] # or pass in your own array of gcode lines instead of reading from a file
#Transform the previous list into an object, this object has some properties to allow the printing process
gcode = gcoder.LightGCode(gcode)

p.startprint(gcode) # this will start a print

i=0;
while(p.printing):
    if i%100==0:
        p.send_now("M105")
        print(p.readline_buf)
    else:
        i+=1
    
    
#If you need to interact with the printer:
p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
print('No')

p.pause() # use these to pause/resume the current print
p.resume()
p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.


print("done")
