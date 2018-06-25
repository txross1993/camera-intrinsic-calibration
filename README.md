# How to use this calibration program
## Supply the config.json file
    ```{
    	"StreamSrc": "ProvideLinkToStream",
    	"CameraMakeAndModel": "ProvideCameraMakeAndModel",
    	"CalibrationPhotoDir": "None",
    	"Mode": "[1 or 2]"
	}```

'''StreamSrc''': The source of the stream. Typically 0, 1, or an rtsp link. 0 or 1 refers to the port on your local device for a pibcam or usb integrated camera device. The rtsp format is ```rtsp://<username>:<password>@<host>:<port>```. Port is optional.

'''CameraMakeAndModel''': Provide a unique make and model for the camera you're calibrating. The idea is for any one camera type, there should only be one calibration unless we install cameras with different focal lengths. If so, provide some uniqueness here such as ''Bosch600VR_wide'' or ''AxisQ3151_longFocal'', etc.


'''CalibrationPhotoDir''': Leave this as None if you want the program to create the directory for you in the /data/calibration-photos directory. Otherwise, provide an existing path to the jpeg photos you intend to use for calibration.

'''Mode 1''': Collect images. Use this mode to start a video stream to your stream source, and press "g" to save the images to the specified CalibrationPhotoDir.

'''Mode 2''': Run calibration. Output pickeled calibration file will be located at data/calibration-files/<CameraMakeAndModel>.calibration.file.