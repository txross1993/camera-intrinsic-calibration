# How to use this calibration program
## Installing requirements
pip install -r requirements.txt

You may have to  manually install some libraries using pip install [module-name]

## Supply the config.json file
    ```
	{
    	"StreamSrc": "ProvideLinkToStream",
    	"CameraMakeAndModel": "ProvideCameraMakeAndModel",
    	"CalibrationPhotoDir": "None",
		"CalibrationPatternSize": "(4,11)",
    	"Mode": "[1, 2, or 3]",
		"CalibrationFile": "Provide the name of the calibration file under /data/CalibrationFiles",
    	"ImageComparisonPath": "Provide the relative path to the project root to the image you want to compare between the original and undistorted images"
	}
	```

**StreamSrc**: The source of the stream. Typically 0, 1, or an rtsp link. 0 or 1 refers to the port on your local device for a pibcam or usb integrated camera device. The rtsp format is ```rtsp://<username>:<password>@<uri>```. 

**CameraMakeAndModel**: Provide a unique make and model for the camera you're calibrating. The idea is for any one camera type, there should only be one calibration unless we install cameras with different focal lengths. If so, provide some uniqueness here such as *Bosch600VR_wide* or *AxisQ3151_longFocal*, etc.

**CalibrationPatternSize**: If using circle grid, found [here](https://docs.opencv.org/2.4/_downloads/acircles_pattern.png), then pattern size is a tuple of "(4,11)" Must be a string in tuple format.

**CalibrationPhotoDir**: Leave this as None if you want the program to create the directory for you in the /data/calibration-photos directory. Otherwise, provide an existing path to the jpeg photos you intend to use for calibration.

**Mode 1**: Collect images. Use this mode to start a video stream to your stream source, and press "g" to save the images to the specified CalibrationPhotoDir.

**Mode 2**: Run calibration. Output pickeled calibration file will be located at data/calibration-files/<CameraMakeAndModel>.calibration.file.

**Mode 3**: Test calibration undistortion output. Provide the path to the image you want to test the undistortion on in ImageComparisonPath and the name of the calibration file located in /data/calibrationFiles.

**CalibrationFile**: If in mode 3, provide the **name** of the calibration file, which must be located in the relative path to root dir, /data/calibrationFiles/<yourCalibrationFileName>.

**ImageComparisonPath**: Provide the full or relative path to the root directory to the image you wish to see in its original format compared to its undistorted format, use this in mode 3 to validate your calibration matrix.