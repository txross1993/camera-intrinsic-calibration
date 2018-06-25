# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:49:36 2018

@author: rossth
"""

import cv2
import os
from Stream.VideoStream import videoStream



class PressGToCaptureFrame(object):
    def __init__(self, streamSrc, calibrationPhotoDir):
        self.src = streamSrc
        self.calibrationPhotoDir = calibrationPhotoDir
        self.cap = self.getVideoStream()

    def saveImg(self, frame, iteration):
        photoDir = os.path.abspath(self.calibrationPhotoDir)
        filename = 'chessboard_{}.jpeg'.format(str(iteration))
        fullPath = os.path.join(photoDir, filename)
        cv2.imwrite(fullPath, frame)
        return
        
    def getVideoStream(self):    
        cap = videoStream(self.src)
        return cap

        