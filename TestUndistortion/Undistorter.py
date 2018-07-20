import cv2
import logging

class VideoFrameUndistorter:
    def __init__(self, frame, mtx, dist):
        self.h, self.w = frame.shape[:2]
        self.mtx = mtx
        self.dist = dist
        self.newcameramtx = None
        self.roi = None

        self.setNewCameraMtx()

    def setNewCameraMtx(self):
        self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx,self.dist, (self.w,self.h), 1, (self.w,self.h))

    def undistort(self, frame):
        """
        Check if the frame's shape has the same dimensions as the initialized frame. If not, update self.h, w, newcameramtx, and roi
        Else, undistort the frame given the provided camera matrix and distortion coefficients
        """
        h, w = frame.shape[:2]
        if h != self.h and w != self.w:
            self.h = h
            self.w = w
            self.setNewCameraMtx()
    
        mapx,mapy = cv2.initUndistortRectifyMap(self.mtx,self.dist,None, self.newcameramtx,(w,h),5)
        undistorted = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)

        #undistorted = cv2.undistort(frame, self.mtx, self.dist, None, self.newcameramtx)
        x,y,w,h = self.roi
        undistorted = undistorted[y:y+h, x:x+w]
        return undistorted

