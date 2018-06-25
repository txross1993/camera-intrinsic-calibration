# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:49:36 2018

@author: rossth
"""

import cv2
import numpy as np
from VideoStream import videoStream
from Undistorter import UndistortImage
import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--username", type=str,
        help="The username to authenticate with on the stream")
    ap.add_argument("-p", "--password", type=str,
        help="The password to authenticate with on the stream")
    ap.add_argument("-url", "--url", type=str,
        help="The uRL of the stream")
    ap.add_argument("-port", "--port", type=int, default=554,
        help="The port for the stream")
    args = vars(ap.parse_args())
    return args

    
def main():    
    #Parse arguments for creating the capture stream
    args = parse_args()
    #Initialize capture class
    cap = videoStream(args["username"], args["password"], args["url"], args["port"])
    
    #Initialize undistorter class, load calibration file and measurements
    unwarp = UndistortImage()
    
    distortion = np.array([[-0.47212106, 0.2778216 , -0.00065095, -0.00125005, -0.08787557]])
    intrinsic_matrix = np.array([[1.27864593e+03, 0.00000000e+00, 9.27321170e+02],
                                 [0.00000000e+00, 1.28360851e+03, 5.26712458e+02],
                                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    rms =  0.3801472352820176
                    
    
    unwarp_mtx2 = UndistortImage(mtx=intrinsic_matrix, dist=distortion)
    
    frame = cap.frame
    unwarp.set_newcameramtx(frame)
    unwarp_mtx2.set_newcameramtx(frame)
    
    #Start the real time stream
    cap.start()
    while True:
        frame = cap.read()
        cv2.imshow('VIDEO', frame)
        cv2.imshow('UNWARPED', unwarp.undistort(frame))
        cv2.imshow('UNWARP_SECOND', unwarp_mtx2.undistort(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    

if __name__=='__main__':
    main()