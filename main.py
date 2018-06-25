import cv2
from time import sleep
import keyboard
import imutils
import logging
import os, sys, json

from Calibrate.capture10Frames import PressGToCaptureFrame
from Calibrate.calibrate import Calibrator

class ValidationError(Exception):
    pass

def parseJsonConfigFile(jsonConfigFile):
    with open(jsonConfigFile, mode='rb') as config:
        data = json.loads(config.read())
        config.close()

    if data['Mode'] not in ["1", "2"]:
        argHelper = """
        Please specify either "1" or "2" as your mode of operation.
            Mode 1: Capture frames to calibrate from
            Mode 2: Calibrate on the captured frames
        One would capture frames before calibration, else there are no photos to calibrate from!
        """
        logging.error(argHelper)
        raise ValidationError(argHelper)
    
    return data

def parse_args():
    if len(sys.argv) == 2:
        configFile = sys.argv[1]
        return parseJsonConfigFile(configFile)
    else:
        argHelper = """
        Wrong number of arguments supplied please suppy
            * Path to json configuration file
        """        
        logging.error(argHelper)
        raise ValidationError(argHelper)

def checkIfDirExists(directory):
    return os.path.isdir(directory)

def getCalibrationPhotoDir(cameraMakeModel, providedCalibrationPhotoDir=None):
    if providedCalibrationPhotoDir:
        if(checkIfDirExists):
            calibrationPhotoDir=providedCalibrationPhotoDir
        else:
            logging.error("""Provided configuration for Calibration Photo Directory does not exist: {}. 
                            Please create this directory or double check your configuration arguments.""".format(providedCalibrationPhotoDir))
            sys.exit(1)
    else:
        calibrationPhotoDir = os.path.abspath("data/calibrationPictures/{}".format(cameraMakeModel))
    return calibrationPhotoDir

def getCalibrationFileLocation(cameraMakeModel):
    calibrationDir = os.path.abspath("../data/calibrationFiles")
    filename = "{}.calibration.file".format(cameraMakeModel)
    calibrationFile = os.path.join(calibrationDir, filename)
    return calibrationFile


def checkForExistingCalibrationPhotoDirs(cameraMakeModel):
    photoDir = getCalibrationPhotoDir(cameraMakeModel)
    if os.path.isdir(photoDir):
        return True
    else:
        logging.warning("Directory for calibration files does not exist: {}. Creating".format(photoDir))
        os.mkdir(photoDir)
        return False

def checkForExistingCalibrationFile(cameraMakeModel):
    if os.path.exists(getCalibrationFileLocation(cameraMakeModel)):
        return True
    else:
        return False

def captureFrames(streamSrc, calibrationPhotoDir):
    num_seconds = 1
    frames_captured = 0

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (30,30)
    fontScale              = 2
    fontColor              = (0,0,255)
    lineType               = 3
    
    streamSrc = PressGToCaptureFrame(streamSrc, calibrationPhotoDir)
    cap = streamSrc.cap.start()

    while True:
        frame = cap.read()
        
        cv2.putText(frame,'{}'.format(str(frames_captured)), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        
        resized = imutils.resize(frame,width=640, height=480)

        cv2.imshow('VIDEO', resized)
        num_seconds += 1
        
        if keyboard.is_pressed('g'):
            streamSrc.saveImg(frame, frames_captured)
            frames_captured += 1        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.closeStream()
            cv2.destroyAllWindows()
            break

def calibrate(cameraMakeModel, calibrationFileName, calibrationPhotoDir):
    Calibrator(cameraMakeModel, calibrationFileName, calibrationPhotoDir).calibrate()

def echoArgs(args):
    logging.info(args)

def main():
    args = parse_args()
    CameraMakeAndModel = args['CameraMakeAndModel']
    argCalibrationPhotoDir = None if args['CalibrationPhotoDir'].lower()=='none' else args['CalibrationPhotoDir']
    CalibrationPhotoDir = getCalibrationPhotoDir(CameraMakeAndModel, argCalibrationPhotoDir)
    CalibrationFilePath = getCalibrationFileLocation(CameraMakeAndModel)
    echoArgs(args)

    if args['Mode'] == "1":
        if not checkForExistingCalibrationPhotoDirs(CameraMakeAndModel):
            captureFrames(args['StreamSrc'], CalibrationPhotoDir)
        else:
            logging.error("""Directory exists for specified CameraMakeAndModel or CalibrationPhotoDir . 
            Please provide a unique instance of the make and model you are attempting to calibrate or use one of the existing calibration files.
            Otherwise, delete the existing calibration photo directory, then try your capture images attempt again.""")
            sys.exit(1)
        
    elif args['Mode'] == "2":
        if not checkForExistingCalibrationFile(CameraMakeAndModel):
            calibrate(CameraMakeAndModel, CalibrationFilePath, CalibrationPhotoDir)
        else:
            logging.error("""Calibration file exists for file {}. 
            Please delete or move this file before attempting recalibration or else provide a different, unique CameraMakeAndModel.""".format(CalibrationFilePath))
            sys.exit(1)
    else:
        logging.warning("No valid mode provided. Please provide a mode of 1 (capture images) or 2 (calibrate camera)")
        sys.exit(0)    

if __name__=='__main__':
    main()