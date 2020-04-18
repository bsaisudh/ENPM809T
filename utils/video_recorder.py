# import necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class RasPiCamera:
    def __init__(self):
        # initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        # allow camera to warmup
        time.sleep(1)
        # video writing
        self.out = cv2.VideoWriter('video.avi',
                              cv2.VideoWriter_fourcc(*"XVID"),
                              2,
                              (640, 480))
    
    def capture(self):
        for frame in self.camera.capture_continuous(self.rawCapture,
                                                    format="bgr",
                                                    use_video_port=False):
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, -1)
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            return image
    
    def capture_and_write(self, fpointer = None, parms = None):
        for frame in self.camera.capture_continuous(self.rawCapture,
                                                    format="bgr",
                                                    use_video_port=False):
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, -1)
            if not fpointer:
                image = fpointer(image, *parms)
            self.video_write(image)
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
    
    def video_write(self, image):
        self.out.write(image)
    
    def cleanup(self):
        self.out.release()
        self.camera.close()
    
if __name__ == "__main__":
    cam = RasPiCamera()
    for i in range(30):
        image = cam.capture()
        cv2.imshow("Frame", image)
        cam.video_write(image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cam.cleanup()
        