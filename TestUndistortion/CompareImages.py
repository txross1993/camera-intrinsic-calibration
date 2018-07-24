
from TestUndistortion.Calibration import CameraCalibration
from TestUndistortion.Undistorter import VideoFrameUndistorter
import cv2
import imutils

class ImageComparison(object):
    def __init__(self, calibrationFile, image):
        self.mtx, self.dist = self.__getCalibrationMatrix(calibrationFile)
        self.image = cv2.imread(image)
        self.undistorter = self.setUndistorter()

        print("MTX: {}".format(self.undistorter.mtx))
        print("DIST: {}".format(self.undistorter.dist))
        print("Height: {}".format(self.undistorter.h))
        print("Width: {}".format(self.undistorter.w))

    def __getCalibrationMatrix(self, calibrationFile):
        calibration = CameraCalibration(calibrationFile)
        mtx = calibration.mtx
        dist = calibration.dist
        return mtx, dist

    def setUndistorter(self):
        undistorter = VideoFrameUndistorter(self.image, self.mtx, self.dist)
        return undistorter
    
    def showComparison(self):
        resized = imutils.resize(self.image,width=640, height=480)
        cv2.imshow('ORIGINAL',resized)
        undistorted = self.undistorter.undistort(self.image)

        undistorted_resized = imutils.resize(undistorted,width=640, height=480)
        cv2.imshow('UNDISTORTED', undistorted_resized); cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1)