import numpy as np
import cv2
import glob, os, sys
import pickle
import logging

class Calibrator(object):
    def __init__(self, cameraMakeModel, calibrationFileName, calibrationPhotoDir):
        self.calibrationFileName = calibrationFileName
        self.calibrationPhotoDir = calibrationPhotoDir
        self.cameraMakeModel = cameraMakeModel

    def calibrate(self):

        def __getCalibrationPhotoDirGlob(cameraMakeModel):
            return glob.glob(self.calibrationPhotoDir + "/*.jpeg")

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*9,3), np.float32)
        objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        images = __getCalibrationPhotoDirGlob(self.cameraMakeModel)
        print(images)
        logging.info(images)
        shape = None

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            shape = gray.shape[::-1]

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (6,9),None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (6,9), corners2,ret)
                cv2.imshow('img',img)
                cv2.waitKey(500)

        try:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, shape, None,None)
        except cv2.error:
            logging.error("Poor chessboard images were supplied. Please try capturing images again")
            sys.exit(1)
        
        total_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            total_error += error
            
        mean_error = total_error/len(objpoints)
        
        toBePickled = {
                'ret': ret,
                'mtx': mtx,
                'dist': dist,
                'rvecs': rvecs,
                'tvecs': tvecs,
                'meanError': mean_error
                }

        camera_calibration_file = open(self.calibrationFileName, mode = 'wb')
        pickle.dump(toBePickled, camera_calibration_file)
        camera_calibration_file.close()
        logging.info('Dumped pickled calibration file in at {}'.format(camera_calibration_file))
        
        cv2.destroyAllWindows()
