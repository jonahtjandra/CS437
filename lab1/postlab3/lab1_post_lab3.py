import time
import datetime
from sense_hat import SenseHat
import asyncio
import numpy as np
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls

from gtts import gTTS
import os

import threading

import cv2
picam2=Picamera2()

sense=SenseHat()
sense.clear()

dispW=1280
dispH=720
picam2.preview_configuration.main.size= (dispW,dispH)
## since OpenCV requires RGB configuration we set the same format for picam2. The 888 implies # of bits on Red, Green and Blue
picam2.preview_configuration.main.format= "RGB888"
picam2.preview_configuration.align() ## aligns the size to the closest standard format
picam2.preview_configuration.controls.FrameRate=60 ## set the number of frames per second, this is set as a request, the actual time it takes for processing each frame and rendering a frame can be different
picam2.configure("preview")
picam2.start()
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
vfile = cv2.VideoWriter('output.mp4', fourcc, 20.0, (dispW,dispH))
START_RECORDING = False
temperature=sense.get_temperature()
faceCascade=cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
while True:
    t = sense.get_temperature()
    print(t)
    if abs(t-temperature) > 1.0:
        START_RECORDING = True
    if START_RECORDING:
        frame=picam2.capture_array() ## frame is a large 2D array of rows and cols and at intersection of each point there is an array of three numbers for RGB i.e. [R,G,B] where RGB value ranges from 0 to 255
        key=cv2.waitKey(1) & 0xFF
        frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(frameGray,1.3,5)
        for x,y,w,h in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),3)
            time.sleep(0.1)
        vfile.write(cv2.resize(frame,(dispW,dispH)))
        cv2.imshow("Camera Frame", frame)
        if key ==ord(" "):
            cv2.imwrite("frame-" + str(time.strftime("%H:%M:%S", time.localtime())) + ".jpg", frame)
        if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
            break

vfile.release()

cv2.destroyAllWindows()


