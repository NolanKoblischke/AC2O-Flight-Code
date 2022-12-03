from picamera import PiCamera
import time


class newCamera:

    def __init__(self):
        self.numPhotosTaken = 0
        self.camera = PiCamera()
        #self.camera.resolution = (4056, 3040) # High Resolution
        self.camera.resolution = (3280, 2464)

    def take_photo(self):
        
        #camera.resolution = (3280, 2464) # Low Resolution
        
        self.camera.start_preview()
        self.camera.awb_mode = 'auto'
        time.sleep(0.05)
        self.camera.exposure_mode ='auto'
        t = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
        self.camera.capture('/home/pi/AC2O/imgs/imageExposure{}.jpg'.format(timestamp))
        self.camera.stop_preview()
        
        self.numPhotosTaken += 1
        print("Photo taken, saved as imageExposure{}.jpg".format(timestamp))
