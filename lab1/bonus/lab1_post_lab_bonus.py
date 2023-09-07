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
FLASH_ON = [[255,255,255] for i in range(64)]
FLASH_OFF = [[0,0,0] for i in range(64)]
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smileCascade=cv2.CascadeClassifier("./haarcascade_smile.xml")
while True:
    frame=picam2.capture_array()
    cv2.imshow("Camera Frame", frame)
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frameGray, 1.1, 8)
    for (x, y, w, h) in faces:
        rof = frameGray[y:y + h, x:x + w] # just get one smile on the last face
        smile_rects, rejectLevels, levelWeights = smileCascade.detectMultiScale3(
                                                            rof, 2.5, 20, outputRejectLevels=True)
        if len(levelWeights) and max(levelWeights) >= 2.0:
            sense.set_pixels(FLASH_ON)
            time.sleep(0.1)
            sense.set_pixels(FLASH_OFF)
            cv2.imwrite("frame-" + str(time.strftime("%H:%M:%S", time.localtime())) + ".jpg", frame)
            exit()
        break
    key=cv2.waitKey(1) & 0xFF
    if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
        break



cv2.destroyAllWindows()



