import cv2
import logging
from threading import Thread

class videoStream:
    """
    Create a CV2 video stream capture by providing the following information:
        username[str] - The username to authenticate with. For the bosch cameras, it's user live
        password[str] - The password for the authenticating user
        streamURL[str] - The ip address or hostname of the device
        port[int] - The port of the stream, which is 554 by default for the bosch cameras
    
    """
    def __init__(self,src):
        self.stream = None
        self.src = src
        self.stopped = False
        self.setStream()
        (self.grabbed, self.frame) = self.stream.read()
        
    def setStream(self):
        cap = cv2.VideoCapture(self.src)
        if cap.isOpened()==True:
            self.stream = cap
        else:
            logging.ERROR("""Video capture failed to open. \n
                          Please check connectivity and authentication parameters for device stream""")
            
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
    
    def getProperty(self, propId):
        return cv2.GetCaptureProperty(self.stream, propId)
    
    def setProperty(self, propId, value):
        cv2.SetCaptureProperty(self.stream, propId, value)
    
    def closeStream(self):
        self.stream.release()