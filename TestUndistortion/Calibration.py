import os
import pickle
import logging

class CameraCalibration:
    def __init__(self, cameraCalibrationFile):
        """
        Calibration file is assumed to be located in the /data/calibration-files folder. 
        Provide the name of the dictionary file you wish to load.
        """
        self.mtx = None # Intrinsic camera parameters
        self.dist = None # Distortion coefficients
        self.rvecs = None # Rotation matrix
        self.tvecs = None # Translation vector

        def _unpickle(filename):             
            with open(filename, mode='rb') as binary:
                unpickled = pickle.load(binary, encoding='latin1')
                binary.close()
            return unpickled


        def _load_calibration(filename):
            script_dir = os.path.dirname(__file__)
            if os.name == 'nt':
                relpath = "..\\data\\calibrationFiles\\{}".format(filename)
            else:
                relpath = "../data/calibrationFiles/{}".format(filename)
            location = os.path.join(script_dir, relpath)

            try:
                unpickedDictionary = _unpickle(location)
                return unpickedDictionary
            except FileNotFoundError as error:
                logging.error(error)
                raise
            

        def _loadCalibrationParameters(unpickledCalibrationFile):
            self.mtx = unpickledCalibrationFile['mtx']
            self.dist = unpickledCalibrationFile['dist']
            self.rvecs = unpickledCalibrationFile['rvecs']
            self.tvecs = unpickledCalibrationFile['tvecs']

        unpickledCalibrationFile = _load_calibration(cameraCalibrationFile)
        _loadCalibrationParameters(unpickledCalibrationFile)

    